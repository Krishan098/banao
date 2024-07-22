from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('doctor_dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})

@login_required
def list_blog_posts(request):
    blog_posts = BlogPost.objects.filter(draft=False)
    return render(request, 'blog/list_blog_posts.html', {'blog_posts': blog_posts})

@login_required
def list_blog_posts_by_category(request, category):
    # Filter blog posts by category
    blog_posts = BlogPost.objects.filter(category=category, draft=False)
    context = {
        'blog_posts': blog_posts,
        'category': category,
    }
    return render(request, 'blog/list_blog_posts_by_category.html', context)