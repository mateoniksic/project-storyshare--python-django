from urllib.parse import urlencode
from django.views import generic

from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from .models import *

from .forms import *
from django.contrib import messages

from .utils.functions import *
from django.core.paginator import Paginator

import time


class IndexTemplateView(generic.TemplateView):
    template_name = 'app/pages/public/index.html'

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
    form_class = CustomUserCreationForm

    template_name = 'app/pages/public/user_auth/sign_up.html'

    success_url = reverse_lazy('app:sign-in')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:for-you-post-list-view'))
        return super().get(request, *args, **kwargs)


class UserSignInView(LoginView):
    template_name = 'app/pages/public/user_auth/sign_in.html'
    form_class = CustomAuthenticationForm

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


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'app/pages/private/user/user_form/user_update_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your user settings have been updated.')
        return response

    def get_success_url(self):
        return reverse_lazy('app:user-update-view', kwargs={'pk': self.object.pk})


class SearchUserProfileListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = 'members'

    template_name = 'app/pages/private/user_profile/user_profile_list/search.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            queryset = User.objects.filter(username__icontains=query).all()
        else:
            queryset = User.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        members = self.object_list
        context['title'] = f'Search results ({len(members)})'

        params_get = self.request.GET.dict()
        filtered_params = {key: value for key,
                           value in params_get.items() if key != 'page'}
        encoded_params = urlencode(filtered_params, safe='&')
        context['params'] = encoded_params + '&'

        return context


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    context_object_name = 'user_profile'

    template_name = 'app/pages/private/user_profile/user_profile_detail/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        member = self.object.user

        if (member == user):
            member = user
            context['is_user'] = True
            context['user_profile_form'] = UserProfileForm(
                instance=self.object)

        context['member'] = member

        posts = member.profile.posts.order_by(
            '-date_created').all()
        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)
        context['posts'] = p.get_page(page)

        return context

    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        request_data = self.request.POST
        user = self.request.user

        form_id = request_data['form_id']

        member_follow_form_id = 'MemberFollowForm'
        if form_id == member_follow_form_id:
            user_action = request_data[f'{member_follow_form_id}-submit']
            user_id = user.id
            member_id = request_data[f'{member_follow_form_id}-member_id']
            member_follow_or_unfollow(user_action, user_id, member_id)

        elif form_id == UserProfileForm().prefix:
            form = UserProfileForm(
                request_data, instance=user.profile)
            if form.is_valid():
                form.save()
                context['user_profile_form'] = UserProfileForm(
                    instance=user.profile)
                context['user'] = user

        return render(request, self.template_name, context=context)


class FollowingPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'app/pages/private/post/post_list/following.html'
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

    template_name = 'app/pages/private/post/post_list/for_you.html'
    paginate_by = 6

    def get_queryset(self):
        following = UserProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()

        queryset = Post.objects.exclude(user_profile__in=following).order_by(
            '-date_created').all()

        return queryset


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'

    template_name = 'app/pages/private/post/post_detail/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        member = self.object.user_profile.user

        if (member == user):
            member = user
            context['is_user'] = True
            context['user_profile_form'] = UserProfileForm(
                instance=user.profile)

        context['member'] = member

        return context

    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        request_data = self.request.POST
        user = self.request.user

        form_id = request_data['form_id']

        member_follow_form_id = 'MemberFollowForm'
        if form_id == member_follow_form_id:
            user_action = request_data[f'{member_follow_form_id}-submit']
            user_id = user.id
            member_id = request_data[f'{member_follow_form_id}-member_id']
            member_follow_or_unfollow(user_action, user_id, member_id)

        elif form_id == UserProfileForm().prefix:
            form = UserProfileForm(
                request_data, instance=user.profile)
            if form.is_valid():
                form.save()
                context['user_profile_form'] = UserProfileForm(
                    instance=user.profile)
                context['user'] = user

        return render(request, self.template_name, context=context)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm

    template_name = 'app/pages/private/post/post_form/post_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm

    template_name = 'app/pages/private/post/post_form/post_update_form.html'

    def get_initial(self):
        tag_list = ' '.join(
            list(self.object.tags.all().values_list('name', flat=True)))
        initial = {
            'tag_list': tag_list
        }
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse_lazy('app:post-detail-view', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse_lazy('app:profile-detail-view', kwargs={'slug': self.request.user.profile.slug})


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
    context_object_name = 'tag'

    template_name = 'app/pages/private/tag/tag_detail/tag_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.object.posts.order_by(
            '-date_created').all()

        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)

        context['posts'] = p.get_page(page)

        return context
