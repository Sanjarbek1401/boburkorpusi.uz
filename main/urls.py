from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Schema uchun sozlama
schema_view = get_schema_view(
    openapi.Info(
        title="Babur Corpus API",
        default_version='v1',
        description="API for Babur's literary works and related information",
        contact=openapi.Contact(email="your@email.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Yo‘llarni belgilash
urlpatterns = [
    path('', views.home, name='home'),
    path('author/', views.author, name='author'),
    path('divan/', views.divan, name='divan'),
    path('divan/category/<int:category_id>/', views.divan_category, name='divan_category'),
    path('divan/text/<int:group_id>/', views.divan_text_detail, name='divan_text_detail'),
    path('divan/work/<int:work_id>/', views.work_detail, name='work_detail'),
    path('baburnoma/', views.baburnoma, name='baburnoma'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('lugatlar/', views.dictionary_list, name='dictionary_list'),

    # Swagger va Redoc uchun
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
