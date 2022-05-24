from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.utils import timezone
# Create your views here.


def post_list(request):
    posts = Post.objects.all().order_by('-published_at')
    return render(request, 'blog/post_list.html', {"posts":posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_at = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit= False)
            post.author = request.user
            post.published_at = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})


def post_draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True).order_by('created_at')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

def post_publish(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form':form})

def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    print(comment)
    comment.approve()
    return redirect('post_list')

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    print(comment)
    comment.delete()
    return redirect('post_detail',pk=comment.post.pk)
