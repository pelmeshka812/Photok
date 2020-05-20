from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from blog import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('blog/', include(urls)),
    path('', TemplateView.as_view(template_name='user/home.html'), name='home'),
]
