from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, login_page, logout_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home-view'),
    path('tutoring/', include('profiles.urls', namespace='profiles')),
    path('choice/', include('cprofiles.urls', namespace='cprofiles')),
    path('mentoring/', include('mprofiles.urls', namespace='mprofiles')),
    path('accounts/login/', login_page, name="login"),
    path('account/logout/', logout_user, name="logout"),
    path('middleschool/', include('middleschool.urls', namespace='middleschool')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
