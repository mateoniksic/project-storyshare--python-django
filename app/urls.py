from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index-template-view'),

    path('sign-up/', views.UserSignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.UserSignInView.as_view(), name='sign-in'),
    path('sign-out/', views.UserSignOutView.as_view(), name='sign-out'),

    path('for-you/', views.ForYouPostListView.as_view(), name='for-you-post-list-view'),
    path('following/', views.FollowingPostListView.as_view(), name='following-post-list-view'),

    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail-view'),
    path('post/create', views.PostCreateView.as_view(), name='post-create-view'),
    path('post/<slug:slug>/update', views.PostUpdateView.as_view(), name='post-update-view'),
    path('post/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post-delete-view'),

    path('user/<int:pk>/update', views.UserUpdateView.as_view(), name='user-update-view'),

    path('profile/<slug:slug>/', views.UserProfileDetailView.as_view(), name='profile-detail-view'),


    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag-detail-view'),

    path('search/member/', views.SearchUserProfileListView.as_view(), name='search-member-list-view'),
]
