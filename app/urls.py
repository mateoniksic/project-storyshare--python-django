from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index-template-view'),

    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),

    path('home/', views.HomePostListView.as_view(), name='home-post-list-view'),
    path('explore/', views.ExplorePostListView.as_view(), name='explore-post-list-view'),

    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail-view'),

    path('<slug:slug>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),
    path('<slug:slug>/update/profile/', views.ProfileUpdateView.as_view(), name='profile-update-view'),

    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag-detail-view'),
]
