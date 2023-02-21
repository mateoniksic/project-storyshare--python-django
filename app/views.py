from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.views.generic import TemplateView, ListView, DetailView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import *
from .forms import *


class PublicIndexPostListView(ListView):
    model = Post

    context_object_name = 'Post'
    queryset = Post.objects.all().order_by('date_created')[:100]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        return context

    template_name = 'app/pages/public/index.html'
    paginate_by = 6

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:private-index'))

        return super().dispatch(*args, **kwargs)


def public_account_sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:private-index'))

    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect(reverse('app:public-sign-in'))

        context = {'form': form}
        return render(request, 'app/pages/public/account/sign_up.html', context=context)


def public_account_sign_in(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:private-index'))

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next = request.GET.get('next')

            if next:
                return redirect(next)
            else:
                return redirect(reverse('app:private-index'))

        else:
            message = 'Your username or password was incorrect. Please, try again.'
            messages.error(request, message)
            return render(request, 'app/pages/public/account/sign_in.html')

    else:
        return render(request, 'app/pages/public/account/sign_in.html')


def private_account_sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('app:public-sign-in'))

    else:
        return redirect(reverse('app:public-sign-in'))


class PrivateIndexPostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        following = CreatorProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()
        queryset = Post.objects.filter(creator_profile__in=following).order_by(
            'date_created').all()
        return queryset

    template_name = 'app/pages/private/index.html'
    paginate_by = 6


class PrivatePostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_active__creator_profile = self.request.user.CreatorProfile
        user__creator_profile__followers = self.object.creator_profile.followers.all()
        context['following'] = user_active__creator_profile in user__creator_profile__followers
        
        user__creator_profile = self.object.creator_profile.user
        context['user__creator_profile'] = user__creator_profile

        return context

    template_name = 'app/pages/private/post.html'


class PrivateExplorePostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        following = CreatorProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()
        queryset = Post.objects.exclude(creator_profile__in=following).order_by(
            'date_created').all()
        return queryset

    template_name = 'app/pages/private/explore.html'
    paginate_by = 6


class PrivateProfileDetailView(LoginRequiredMixin, DetailView):
    model = CreatorProfile
    context_object_name = 'CreatorProfileDetail'
    template_name = 'app/pages/private/profile.html'
