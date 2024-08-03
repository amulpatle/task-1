from django.shortcuts import render, redirect
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from .models import BlogPost
# Create your views here.

@login_required
def createblog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid form')
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('my_blog_posts')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }
    return render(request, 'createblog.html', context)


@login_required
def my_blog_posts(request):
    blog_posts = BlogPost.objects.filter(author=request.user)
    categories = BlogPost.CATEGORY_CHOICES
    context = {
        'posts': blog_posts,
        'categories':categories,
    }
    return render(request, 'my_blog_posts.html', context)