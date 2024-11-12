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
    path('authors/', views.AuthorInfoAPIView.as_view(), name='author-info'),
    path('baburnoma/', views.BaburnomaAPIView.as_view(), name='baburnoma'),
    path('divan-categories/', views.DivanCategoryAPIView.as_view(), name='divan-categories'),
    path('categories/<int:id>/', views.DivanCategoryDetailAPIView.as_view(), name='divan-category-detail'),
    path('divan-groups/', views.DivanGroupAPIView.as_view(), name='divan-groups'),
    path('groups/<int:id>/', views.DivanGroupDetailAPIView.as_view(), name='divan-group-detail'),
    path('divan-little-groups/', views.DivanLittleGroupAPIView.as_view(), name='divan-little-groups'),
    path('divan-texts/', views.DivanTextAPIView.as_view(), name='divan-texts'),
    path('contacts/', views.AdminContactAPIView.as_view(), name='contacts'),

    # Swagger va Redoc uchun
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
