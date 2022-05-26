from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from django.core.paginator import Paginator
from .models import Movie, MovieComment
# from .forms import MovieCommentForm
from .forms import MovieCommentForm, MovieCommentUpdateForm
from django.contrib.auth.decorators import login_required
import requests
import json


@require_safe
def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': page_obj,
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment_form = MovieCommentForm()
    comments = movie.moviecomment_set.all()
    context = {
        'movie': movie,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'movies/detail.html', context)


prev_movies = []


@require_http_methods(['GET', 'POST'])
def recommended(request):
    if request.method == 'POST':
        global prev_movies
        recoinput = json.loads(request.body)['recoinput']
        movies = Movie.objects.all()
        movie_titles = []
        selected_title = '쇼생크 탈출'
        max_similarity = 0
        for movie in movies:
            movie_titles.append(movie.title)
        for title in movie_titles:
            similarity = LCS(title, recoinput)
            if max_similarity < similarity:
                max_similarity = similarity
                selected_title = title
        BASE_URL = 'https://api.themoviedb.org/3'
        params = {
            'api_key': 'e3c35f43a5d9b9abad66e9b03314455e',
            'language': 'ko',
            'region': 'KR',
            'query': selected_title,
        }
        path = '/search/movie'

        response = requests.get(BASE_URL + path, params=params).json()
        results = response.get('results')

        if len(results):
            movie_id = results[0].get('id')
        else:
            return render(request, 'movies/recommended/')


        path = f'/movie/{movie_id}/recommendations'
        params = {
            'api_key': 'e3c35f43a5d9b9abad66e9b03314455e',
            'language': 'ko',
        }

        response = requests.get(BASE_URL + path, params=params).json()
        results = response.get('results')
        movies = []
        for result in results:
            overview = result.get('overview')
            movies.append({
                'title': result.get('title'),
                'vote_average': result.get('vote_average'),
                'overview': overview[:120]+'...',
                'poster_path': result.get('poster_path'),
            })
            if len(movies) == 10:
                break
        if movies:
            prev_movies = movies[:]
        else:
            movies = prev_movies[:]
        return JsonResponse(movies, safe=False)

    elif request.method == 'GET':
        return render(request, 'movies/recommended.html' )


def LCS(word_a, word_b):
    dp = [[0]*(len(word_b)+1) for _ in range(len(word_a)+1)]

    for i in range(len(word_a)+1):
        for j in range(len(word_b)+1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif word_a[i-1] == word_b[j-1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    rlt = 0
    for i in range(len(word_a)+1):
        rlt = max(rlt, max(dp[i]))
    return rlt


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        comment_form = MovieCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(MovieComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)