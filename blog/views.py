from django.shortcuts import render
from .models import Post
from django.utils import timezone 
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
import os 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    reviews = Review.objects.order_by('-created_date')
    
    # Combine and sort items
    items = sorted(
        list(posts) + list(reviews), 
        key=lambda x: getattr(x, 'published_date', getattr(x, 'created_date')), 
        reverse=True
    )
    
    return render(request, 'blog/post_list.html', {'items': items})
    


def post_detail (request, pk):
    Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
     if request.method == "POST":
         form = PostForm(request.POST)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm()
     return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'blog/post_edit.html', {'form': form})
@login_required
def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('review_detail', pk=review.pk)
    else:
        form = ReviewForm()
    return render(request, 'blog/create_review.html', {'form': form})

def review_list(request):
    reviews = Review.objects.order_by('-created_date')
    return render(request, 'blog/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'blog/review_detail.html', {'review': review})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})
def custom_logout(request):
    logout(request)
    return redirect('post_list')
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('post_list')
    else:
        # Redireciona se não for o autor
        return redirect('post_detail', pk=post.pk)