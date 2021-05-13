from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, login_page, logout_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home-view'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('cprofiles/', include('cprofiles.urls', namespace='cprofiles')),
    path('accounts/login/', login_page, name="login"),
    path('account/logout/', logout_user, name="logout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
