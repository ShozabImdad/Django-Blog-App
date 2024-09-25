from django.shortcuts import render, get_object_or_404, redirect
from . models import Blog
from . forms import BlogForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def index(request):
    return render(request, 'index.html', {})


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-created_at']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Blog.objects.filter(title__icontains=query) | Blog.objects.filter(text__icontains=query)
        return Blog.objects.all()


# def blog_list(request):
#     if request.method == "GET":
#         q = request.GET.get('q')
#         if q:
#             blogs = Blog.objects.filter(text__icontains=q).order_by('-created_at')
#             blogs = Blog.objects.filter(title__icontains=q).order_by('-created_at')
#         else:
#             blogs = Blog.objects.all()
#     return render(request, 'blog_list.html', {'blogs': blogs})


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = '/blogs/'  # Redirect to blog list after creation

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the current user as blog owner
        return super().form_valid(form)


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

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = '/blogs/'

    def get_object(self, queryset=None):
        return get_object_or_404(Blog, pk=self.kwargs['pk'], user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the current user as blog owner
        return super().form_valid(form)


# class BlogCreateView(LoginRequiredMixin, CreateView):
#     model = Blog
#     form_class = BlogForm
#     template_name = 'blog_form.html'
#     success_url = '/blogs/'  # Redirect to blog list after creation

#     def form_valid(self, form):
#         form.instance.user = self.request.user  # Set the current user as blog owner
#         return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = '/blogs/'

    def get_object(self, queryset=None):
        return get_object_or_404(Blog, pk=self.kwargs['pk'], user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the current user as blog owner
        return super().form_valid(form)


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


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blog_confirm_delete.html'
    success_url = '/blogs/'

    def get_object(self, queryset=None):
        return get_object_or_404(Blog, pk=self.kwargs['pk'], user=self.request.user)


# @login_required
# def blog_delete(request, blog_id):
#     blog = get_object_or_404(Blog, pk = blog_id, user = request.user)
#     if request.method == 'POST':
#         blog.delete()
#         return redirect('blog_list')
#     return render(request, 'blog_confirm_delete.html', {'blog': blog})


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = '/blog_list/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(self.request, user)
        return super().form_valid(form)


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