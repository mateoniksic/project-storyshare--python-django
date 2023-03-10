from urllib.parse import urlencode
from django.views import generic

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from .models import *

from .forms import *
from django.contrib import messages

from .utils.mixins import *
from django.core.paginator import Paginator


class IndexTemplateView(generic.TemplateView):
    template_name = 'app/pages/public/IndexTemplateView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().order_by('-date_created')[:18]
        context['posts_total'] = Post.objects.all().count()

        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)

        context['posts'] = p.get_page(page)

        return context

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:for-you-post-list-view'))

        return super().dispatch(*args, **kwargs)


class UserSignUpView(generic.CreateView):
    model = User
    form_class = UserForm

    template_name = 'app/pages/public/member/sign_up.html'

    success_url = reverse_lazy('app:sign-in')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:for-you-post-list-view'))
        return super().get(request, *args, **kwargs)


class UserSignInView(LoginView):
    template_name = 'app/pages/public/member/sign_in.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('app:for-you-post-list-view')

    def form_invalid(self, form):
        messages.error(
            self.request, 'Your username or password was incorrect. Please, try again.')
        return self.render_to_response(self.get_context_data(form=form))


class UserSignOutView(LogoutView):
    next_page = reverse_lazy('app:sign-in')


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
