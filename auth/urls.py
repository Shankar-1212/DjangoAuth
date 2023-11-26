from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from users import views
from django.urls.conf import include  
from django.conf import settings  
from django.conf.urls.static import static  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('doctor_home/', user_views.doctor_home, name='doctor_home'),
    path('signup/', user_views.signup, name='signup'),
    path('login/',user_views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
        