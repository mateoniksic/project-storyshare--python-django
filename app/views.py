from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.models import User
from .models import *
from .forms import *


class IndexTemplateView(generic.TemplateView):
    # model = Post

    # context_object_name = 'Post'
    # queryset = Post.objects.all().order_by('date_created')[:100]

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_count'] = len(Post.objects.all())
    #     return context

    template_name = 'app/pages/public/index.html'
    # paginate_by = 6

    # def dispatch(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return redirect(reverse('app:private-index'))

    #     return super().dispatch(*args, **kwargs)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:home'))

    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect(reverse('app:sign-in'))

        context = {'form': form}
        return render(request, 'app/pages/public/member/sign_up.html', context=context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:home'))

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
                return redirect(reverse('app:home'))

        else:
            message = 'Your username or password was incorrect. Please, try again.'
            messages.error(request, message)
            return render(request, 'app/pages/public/member/sign_in.html')

    else:
        return render(request, 'app/pages/public/member/sign_in.html')


def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('app:sign-in'))

    else:
        return redirect(reverse('app:sign-in'))


class HomePostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'app/pages/private/HomePostListView.html'
    paginate_by = 6

    def get_queryset(self):
        following = UserProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()

        queryset = Post.objects.filter(user_profile__in=following).order_by(
            'date_created').all()

        return queryset


class ExplorePostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'app/pages/private/ExplorePostListView.html'
    paginate_by = 6

    def get_queryset(self):
        following = UserProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()

        queryset = Post.objects.exclude(user_profile__in=following).order_by(
            'date_created').all()

        return queryset


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'

    template_name = 'app/pages/private/PostDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        member = self.object.user_profile.user
        context['member'] = member

        return context


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    context_object_name = 'user_profile'

    template_name = 'app/pages/private/ProfileDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        member = self.object.user
        context['member'] = member

        posts = member.profile.posts.all()
        context['posts'] = posts

        context['isProfileDetailView'] = True

        return context


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
    context_object_name = 'tag'

    template_name = 'app/pages/private/TagDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.object.posts.all()
        context['posts'] = posts

        return context


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UserProfile
    fields = ['profile_image', 'description']
    template_name = 'app/pages/private/ProfileUpdateView.html'

    def get_success_url(self):
        return reverse('app:profile-detail-view', kwargs={'slug': self.object.slug})
