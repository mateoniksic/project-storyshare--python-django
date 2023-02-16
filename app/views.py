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


class PublicIndexListView(ListView):
    model = Post

    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('date_created')[:18]
    extra_context = {'posts_count': len(Post.objects.all())}

    paginate_by = 6

    template_name = 'app/pages/public/index.html'

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


class PrivateIndexListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        following = CreatorProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()
        queryset = Post.objects.filter(creator_profile__in=following).order_by(
            'date_created').all()
        return queryset

    paginate_by = 6

    template_name = 'app/pages/private/index.html'


class PrivatePostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/pages/private/post/single_post.html'


class PrivateExploreListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        following = CreatorProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()
        queryset = Post.objects.exclude(creator_profile__in=following).order_by(
            'date_created').all()
        return queryset

    paginate_by = 6

    template_name = 'app/pages/private/explore.html'
