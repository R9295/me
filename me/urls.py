"""me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('theme/', include(('themes.urls', 'themes'), namespace='themes')),
    path('coupons/', include(('coupons.urls', 'coupons'), namespace='coupons')),
    path('', include(('feedback.urls', 'feedback'), namespace='feedback')),
    path('feeds/', include(('feeds.urls', 'feeds'), namespace='feeds')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ERROR HANDLERS for production
handler400 = 'me.views.handler400'
handler403 = 'me.views.handler403'
handler404 = 'me.views.handler404'
handler500 = 'me.views.handler500'
