from django.shortcuts import render, get_object_or_404
from .models import Blog  

# Blog list page
def blog_list(request):
    blogs = Blog.objects.filter(published=True).order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

# Blog detail page
def blog_detail(request, slug):
    blog_post = get_object_or_404(Blog, slug=slug, published=True)
    return render(request, 'blog/blog_detail.html', {'blog': blog_post})
