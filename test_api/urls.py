from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from test_api import views


router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('review', views.ReviewViewSet)
router.register('', views.filmViewSet)


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)), 
    path('profile/<int:pk>/update_fav_genre/', views.updateFavGenre.as_view()),
    path('<int:pk>/upvote', views.upvote.as_view()),
    path('<int:pk>/downvote', views.downvote.as_view()),
    

   
]
