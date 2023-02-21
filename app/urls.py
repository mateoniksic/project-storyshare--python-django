from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.PublicIndexPostListView.as_view(), name='public-index'),
    path('sign-up/', views.public_account_sign_up, name='public-sign-up'),
    path('sign-in/', views.public_account_sign_in, name='public-sign-in'),
    path('sign-out/', views.private_account_sign_out, name='private-sign-out'),
    path('home/', views.PrivateIndexPostListView.as_view(), name='private-index'),
    path('explore/', views.PrivateExplorePostListView.as_view(),
         name='private-explore'),
    path('post/<slug:slug>', views.PrivatePostDetailView.as_view(),
         name='private-post-detail-view'),
    path('profile/<slug:slug>', views.PrivateProfileDetailView.as_view(),
         name='private-profile-detail-view'),
]
