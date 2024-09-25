from django.shortcuts import render, get_object_or_404, redirect
from . models import Blog
from . forms import BlogForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def index(request):
    return render(request, 'index.html', {})


class BlogListView(View):
    def get(self, request):
        if request.method == "GET":
            q = request.GET.get('q')
            if q:
                blogs = Blog.objects.filter(text__icontains=q).order_by('-created_at')
                blogs = Blog.objects.filter(title__icontains=q).order_by('-created_at')
            else:
                blogs = Blog.objects.all()
        return render(request, 'blog_list.html', {'blogs': blogs})


# def blog_list(request):
#     if request.method == "GET":
#         q = request.GET.get('q')
#         if q:
#             blogs = Blog.objects.filter(text__icontains=q).order_by('-created_at')
#             blogs = Blog.objects.filter(title__icontains=q).order_by('-created_at')
#         else:
#             blogs = Blog.objects.all()
#     return render(request, 'blog_list.html', {'blogs': blogs})


class BlogCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = BlogForm()
        return render(request, 'blog_form.html', {'form': form})
    
    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit = False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
        return render(request, 'blog_form.html', {'form': form})
    


# @login_required
# def blog_create(request):
#     if request.method == 'POST':
#         form = BlogForm(request.POST, request.FILES)
#         if form.is_valid():
#             blog = form.save(commit = False)
#             blog.user = request.user
#             blog.save()
#             return redirect('blog_list')
#     else:
#         form = BlogForm()
#     return render(request, 'blog_form.html', {'form': form})




class BlogUpdateView(LoginRequiredMixin, View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk = blog_id, user = request.user)
        form = BlogForm(request.POST, request.FILES, instance = blog)
        return render(request, 'blog_form.html', {'form': form})
    
    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, pk = blog_id, user = request.user)
        form = BlogForm(request.POST, request.FILES, instance = blog)
        if form.is_valid():
            blog = form.save(commit = False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
        return render(request, 'blog_form.html', {'form': form})


# @login_required
# def blog_edit(request, blog_id):
#     blog = get_object_or_404(Blog, pk = blog_id, user = request.user)
#     if request.method == "POST":
#         form = BlogForm(request.POST, request.FILES, instance = blog)
#         if form.is_valid():
#             blog = form.save(commit = False)
#             blog.user = request.user
#             blog.save()
#             return redirect('blog_list')
#     else:
#         form = BlogForm(instance = blog)
#     return render(request, 'blog_form.html', {'form': form})


class BlogDeleteView(LoginRequiredMixin, View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
        return render(request, 'blog_confirm_delete.html', {'blog': blog})
    
    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
        blog.delete()
        return redirect('blog_list')


# @login_required
# def blog_delete(request, blog_id):
#     blog = get_object_or_404(Blog, pk = blog_id, user = request.user)
#     if request.method == 'POST':
#         blog.delete()
#         return redirect('blog_list')
#     return render(request, 'blog_confirm_delete.html', {'blog': blog})


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form}) 
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('blog_list')
        return render(request, 'registration/register.html', {'form': form}) 

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             login(request, user)
#             return redirect('blog_list')
#     else:
#         form = UserRegistrationForm()
    
#     return render(request, 'registration/register.html', {'form': form}) 

