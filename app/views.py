from urllib.parse import urlencode
from django.views import generic

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from .models import *

from .forms import *
from django.contrib import messages

from .contrib.mixins import *
from django.core.paginator import Paginator


class IndexTemplateView(generic.TemplateView):
    template_name = 'app/pages/public/IndexTemplateView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-date_created')[:6]
        context['posts_total'] = len(Post.objects.all())
        return context

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:for-you-post-list-view'))

        return super().dispatch(*args, **kwargs)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:for-you-post-list-view'))

    else:
        form = UserForm()

        if request.method == 'POST':
            form = UserForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect(reverse('app:sign-in'))

        context = {'form': form}
        return render(request, 'app/pages/public/member/sign_up.html', context=context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:for-you-post-list-view'))

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
                return redirect(reverse('app:for-you-post-list-view'))

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


class FollowingPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'app/pages/private/FollowingPostListView.html'
    paginate_by = 6

    def get_queryset(self):
        following = UserProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()

        queryset = Post.objects.filter(user_profile__in=following).order_by(
            '-date_created').all()

        return queryset


class ForYouPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'app/pages/private/ForYouPostListView.html'
    paginate_by = 6

    def get_queryset(self):
        following = UserProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()

        queryset = Post.objects.exclude(user_profile__in=following).order_by(
            '-date_created').all()

        return queryset


class PostDetailView(LoginRequiredMixin, FollowMemberMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'

    template_name = 'app/pages/private/PostDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        member = self.object.user_profile.user
        context['member'] = member

        if (member == self.request.user):
            context['has_perms'] = True

        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm

    template_name = 'app/pages/private/PostForm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_submit_value'] = 'Create a new story'
        context['icon'] = 'plus-circle'

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm

    template_name = 'app/pages/private/PostForm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_submit_value'] = 'Update story'
        context['icon'] = 'edit'

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        tag_list = list(self.object.tags.all().values_list('name', flat=True))
        tag_list = ' '.join(tag_list)
        initial = {
            'tag_list': tag_list
        }
        return initial

    def get_success_url(self):
        return reverse_lazy('app:post-detail-view', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse_lazy('app:profile-detail-view', kwargs={'slug': self.request.user.profile.slug})


class ProfileDetailView(LoginRequiredMixin, FollowMemberMixin, generic.DetailView):
    model = UserProfile
    context_object_name = 'user_profile'

    template_name = 'app/pages/private/ProfileDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        member = self.object.user
        context['member'] = member

        posts = member.profile.posts.order_by(
            '-date_created').all()

        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)

        context['posts'] = p.get_page(page)

        if (member == self.request.user):
            context['has_perms'] = True

        context['isHidden'] = True

        return context


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    # TODO
    model = UserProfile
    fields = ['profile_image', 'description']
    template_name = 'app/includes/member/profile/profile_update.html'

    def get_success_url(self):
        return reverse_lazy('app:profile-detail-view', kwargs={'slug': self.object.slug})


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
    context_object_name = 'tag'

    template_name = 'app/pages/private/TagDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.object.posts.order_by(
            '-date_created').all()

        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)

        context['posts'] = p.get_page(page)

        return context


class SearchMemberListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = 'members'

    template_name = 'app/pages/private/SearchListView.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            queryset = User.objects.filter(
                username__icontains=query).all()
        else:
            queryset = User.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        members = self.object_list
        context['title'] = f'Search results ({len(members)})'

        params_get = self.request.GET.dict()
        params = {
            'q': params_get['q']
        }
        encoded_params = urlencode(params, safe='&')

        context['params'] = encoded_params + '&'

        return context
