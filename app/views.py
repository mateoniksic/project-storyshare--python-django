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
    form_class = CustomUserCreationForm

    template_name = 'app/pages/public/member/UserSignUpView.html'

    success_url = reverse_lazy('app:sign-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_title'] = 'Sign up'
        context['form_submit_value'] = 'Sign up'
        context['form_data_before_submit'] = 'By signing up, you agree to our <a href="" class="link link--text">Terms</a> . Learn how we collect, use and share your data in our <a href="" class="link link--text">Privacy Policy</a> and how we use cookies and similar technology in our <a href="" class="link link--text">Cookies Policy</a>.'

        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:for-you-post-list-view'))
        return super().get(request, *args, **kwargs)


class UserSignInView(LoginView):
    template_name = 'app/pages/public/member/UserSignInView.html'
    form_class = CustomAuthenticationForm

    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_title'] = 'Sign in'
        context['form_submit_value'] = 'Sign in'
        context['form_data_extra'] = 'Don\'t remember password? <a href="#" id="js-btn-forgot-password" class="link link--text"> Reset password </a>'

        return context

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


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'

    template_name = 'app/pages/private/PostDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        member = self.object.user_profile.user
        context['member'] = member

        if (member == self.request.user):
            context['has_perms'] = True

            initial = {
                'profile_image': user.profile.profile_image,
                'description': user.profile.description
            }
            context['UserProfileForm'] = UserProfileForm(initial=initial)

        return context

    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        form_id = self.request.POST.get('form_id')

        member_follow_form_id = 'MemberFollowForm'
        if form_id == member_follow_form_id:
            action = request.POST.get(f'{member_follow_form_id}-submit')
            user_id = request.user.id
            member_id = request.POST.get(
                f'{member_follow_form_id}-member_id')
            member_follow_or_unfollow(action, user_id, member_id)

        elif form_id == UserProfileForm().prefix:
            user_profile_form = UserProfileForm(
                request.POST, instance=self.request.user.profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
                context['UserProfileForm'] = UserProfileForm(
                    instance=self.request.user.profile)
                context['member'] = self.request.user

        return render(request, self.template_name, context=context)


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
        tag_list = ' '.join(
            list(self.object.tags.all().values_list('name', flat=True)))
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


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    context_object_name = 'user_profile'

    template_name = 'app/pages/private/ProfileDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        member = self.object.user
        context['member'] = member

        if (member == user):
            context['has_perms'] = True
            context['isHidden'] = True

            initial = {
                'profile_image': user.profile.profile_image,
                'description': user.profile.description
            }
            context['UserProfileForm'] = UserProfileForm(initial=initial)

        posts = member.profile.posts.order_by(
            '-date_created').all()

        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)

        context['posts'] = p.get_page(page)

        return context

    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        form_id = self.request.POST.get('form_id')

        member_follow_form_id = 'MemberFollowForm'
        if form_id == member_follow_form_id:
            action = request.POST.get(f'{member_follow_form_id}-submit')
            user_id = request.user.id
            member_id = request.POST.get(
                f'{member_follow_form_id}-member_id')
            member_follow_or_unfollow(action, user_id, member_id)

        elif form_id == UserProfileForm().prefix:
            user_profile_form = UserProfileForm(
                request.POST, instance=self.object)
            if user_profile_form.is_valid():
                user_profile_form.save()
                context['UserProfileForm'] = UserProfileForm(
                    instance=self.object)
                context['user'] = self.object.user

        return render(request, self.template_name, context=context)


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
