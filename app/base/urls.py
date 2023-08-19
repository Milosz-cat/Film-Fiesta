"""
URL configuration for movie_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('movie/<str:title>/<str:year>/', views.movie, name="movie"),
    path('person/<str:name>/', views.person, name="person"),
    path('search/', views.search, name="search"),
    path('add_review/<int:movie_id>', views.add_review, name='add_review'),
    path('add_comment/<int:review_id>', views.add_comment, name='add_comment'),
    path('profile_reviews', views.profile_reviews, name='profile_reviews'),
    path('remove_review/<int:pk>', views.remove_review, name='remove_review'),
    path('remove_comment/<int:pk>', views.remove_comment, name='remove_comment'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
