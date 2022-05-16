from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from social.views import inicioView, logoutBaseView, loginBaseView, RegisterView, RegisterCatalogView, \
						RegisterCatalogEditarView, CatalogDeleteView


urlpatterns = [
	path('', inicioView.as_view(), name='inicio'),
	path('register/user/crear', RegisterView.as_view(), name='register_user'),
	path('register/catalog/crear', RegisterCatalogView.as_view(), name='register_catalog'),
	path('register/catalog/<int:id>/editar', RegisterCatalogEditarView.as_view(), name='editar_catalog'),
	path('catalog/<int:id>/delete', CatalogDeleteView.as_view(), name='delete_catalog'),
	path('login/', loginBaseView.as_view(), name='login'),
	path('logout/', logoutBaseView.as_view(), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)