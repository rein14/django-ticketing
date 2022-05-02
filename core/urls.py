"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from app import views


handler403 = views.handler404

urlpatterns = [
    path("select2/", include("django_select2.urls")),
    path('', include('pwa.urls')),
    path('webpush/', include('webpush.urls')),

    path('', include('django.contrib.auth.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),


    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('cms/', include('cms.urls')),
    path('', include('app.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.views import serve
    from django.views.decorators.cache import never_cache
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)