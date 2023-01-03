from . import views
from django.urls import path
from django.conf.urls.static import static
from myapp import settings


urlpatterns = [
    
    path('', views.home),
    path('home/', views.home, name='home'),
    path('about/', views.About, name='about'),
    path('register/', views.Register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('form_Contact/', views.ContactUs, name='contact'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
