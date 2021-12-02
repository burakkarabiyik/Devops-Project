from typing import Dict
from django.shortcuts import render, get_object_or_404
from blog.models import MyCategories, Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseNotFound
from django.db.models import Q
import os;
# Create your views here.


def index(request):
    site=os.environ.get('DJANGO_SITE')
    context = dict()
    posts = Post.objects.all().order_by('id')
    son = Post.objects.all().order_by('-publishing_date')[:3]
    context["son"] = son
    context["posts2"] = Post.objects.all()
    context["kategoriler"] = MyCategories.objects.all()
    context["count"] = Post.objects.count()
    q = request.GET.get('q')
    if q:

        posts = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q))
        context["posts"] = posts
        context["q"] = q
        if len(posts) < 1:
            context["posts3"] = True
    k = request.GET.get('k')
    if k:

        posts = Post.objects.filter(Q(status=k))
        context["posts"] = posts
        context["k"] = k
        if len(posts) < 1:
            context["posts3"] = True

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # posts=paginator.page(paginator.num_pages)
        return HttpResponseNotFound('<h1>Page not found</h1>')
    context["posts"] = posts
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def postdetails(request, slug):
    context = dict()
    post = get_object_or_404(Post, slug=slug)
    post.save()
    son = Post.objects.all().order_by('-publishing_date')[:3]
    context["posts"] = post
    context["son"] = son
    return render(request, 'post-details.html', context)
