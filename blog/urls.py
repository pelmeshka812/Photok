from django.urls import path
from django.views.generic import TemplateView
from blog import views

app_name = 'blog'
urlpatterns = [
    path('main/', TemplateView.as_view(template_name="blog/main.html")),
    path('photos/', views.photo_create, name='photos' ),
    path('like/', views.photo_like, name='like'),
    path('create/', views.photo_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.photo_detail, name='detail'),
    path('', views.photo_like, name='list')

]
