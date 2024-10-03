# -*- coding: utf-8 -*-
# sitewomen\women\views.py
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request: HttpRequest) -> HttpResponse:
    posts = Women.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=data)


def about(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'О сайте',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/about.html', context=data)


def show_post(request: HttpRequest, post_slug: str) -> HttpResponse:
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 0,
    }
    return render(request, 'women/show_post.html', context=data)


def addpage(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Добавление статьи',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/addpage.html', context=data)


def contact(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Обратная связь',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/contact.html', context=data)


def login(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Авторизация',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/login.html', context=data)


def show_category(request: HttpRequest, cat_slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat=category).select_related('cat')
    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.slug,
    }
    return render(request, 'women/show_category.html', context=data)


def show_tag_postlist(request: HttpRequest, tag_slug: str) -> HttpResponse:
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.womens.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f'Тег: {tag.womens}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', context=data)
