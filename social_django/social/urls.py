from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from social.views import inicioView, logoutBaseView, loginBaseView, RegisterView


urlpatterns = [
	#path('', views.inicio, name='inicio'),
	path('', inicioView.as_view(), name='inicio'),
	path('profile/', views.profile, name='profile'),
	path('profile/<str:username>/', views.profile, name='profile'),
	#path('register/', views.register, name='register'),
	path('register/', RegisterView.as_view(), name='register'),
	#path('login/', LoginView.as_view(template_name='base/login.html'), name='login'),
	#path('logout/', LogoutView.as_view(template_name='base/base.html'), name='logout'),
	path('login/', loginBaseView.as_view(), name='login'),
	path('logout/', logoutBaseView.as_view(), name='logout'),
	path('post/', views.post, name='post'),
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)