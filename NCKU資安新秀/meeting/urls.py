"""
URL configuration for meeting project.

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
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path as url
from django.conf.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from dinosaur import views


router = DefaultRouter()
router.register(r'check', views.GroupViewSet)




# urlpatterns = [
#     path('meeting/', include('dinosaur.urls')),
#     path('admin/', admin.site.urls),
#     url(r'^api/', include(router.urls)),
#     #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     url(r'^api/update/', views.update_checkdig, name='update_checkdig'),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

#Local
urlpatterns = [
    path('', include('dinosaur.urls')),
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/update/', views.update_checkdig, name='update_checkdig'),
    url(r'^api/updateisempty/', views.update_isempty, name='update_isempty'),
] 
