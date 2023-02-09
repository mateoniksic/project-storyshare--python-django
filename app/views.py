from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class IndexListView(ListView):
    model = Post

    context_object_name = 'posts'
    queryset = Post.objects.all()
    extra_context = {'posts_count': len(Post.objects.all())}

    paginate_by = 10

    template_name = 'app/pages/index/index.html'

    # def dispatch(self, *args, **kwargs):
    #     if not self.request.user.is_authenticated:
    #         return redirect(reverse('app:sign-in'))
    #     return super().dispatch(*args, **kwargs)


def sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:sign-in'))

    context = {'form': form}
    return render(request, 'app/pages/account/sign_up.html', context=context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('app:index'))
        else:
            message = 'Your username or password was incorrect. Please, try again.'
            messages.error(request, message)
            return render(request, 'app/pages/account/sign_in.html')
    else:
        return render(request, 'app/pages/account/sign_in.html')


def sign_out(request):
    logout(request)
    return redirect(reverse('app:sign-in'))


class CreatorProfileListView(LoginRequiredMixin, ListView):
    model = CreatorProfile
    context_object_name = 'creator_profiles'
    queryset = CreatorProfile.objects.all()
    template_name = 'app/creator_profile/creator_profile_list.html'


class CreatorProfileDetailView(DetailView):
    model = CreatorProfile
    context_object_name = 'creator_profile'
    template_name = 'app/creator_profile/creator_profile_detail.html'


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all()
    template_name = 'app/post/post_list.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post/post_detail.html'


class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'
    queryset = Tag.objects.all()
    template_name = 'app/tag/tag_list.html'


class TagDetailView(DetailView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'app/tag/tag_detail.html'
