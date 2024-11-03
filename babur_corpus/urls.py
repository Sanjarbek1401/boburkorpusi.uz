from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from main.views import (
    AuthorInfoAPIView,
    BaburnomaAPIView,
    DivanCategoryAPIView,
    DivanGroupAPIView,
    DivanLittleGroupAPIView,
    DivanTextAPIView,
    AdminContactAPIView
)

# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="Babur Corpus API",
        default_version='v1',
        description="API documentation for Babur Corpus project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@baburcorpus.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API URLs
    path('api/authors/', AuthorInfoAPIView.as_view(), name='author-info'),
    path('api/baburnoma/', BaburnomaAPIView.as_view(), name='baburnoma'),
    path('api/divan-categories/', DivanCategoryAPIView.as_view(), name='divan-categories'),
    path('api/divan-groups/', DivanGroupAPIView.as_view(), name='divan-groups'),
    path('api/divan-little-groups/', DivanLittleGroupAPIView.as_view(), name='divan-little-groups'),
    path('api/divan-texts/', DivanTextAPIView.as_view(), name='divan-texts'),
    path('api/contacts/', AdminContactAPIView.as_view(), name='contacts'),

    # API authentication
    path('api-auth/', include('rest_framework.urls')),

    # Swagger documentation URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
