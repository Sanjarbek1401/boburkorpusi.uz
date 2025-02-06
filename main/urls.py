from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


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

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
