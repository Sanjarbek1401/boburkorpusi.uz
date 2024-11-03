from django_filters import rest_framework as filters
from .models import DivanCategory


class DivanCategoryFilter(filters.FilterSet):
    group_name = filters.CharFilter(field_name='groups__name',lookup_expr='icontains')
    little_group_name = filters.CharFilter(field_name='groups__little_groups__name',lookup_expr='icontains')
    text_content = filters.CharFilter(field_name='groups__little_groups__texts__text',lookup_expr='icontains')

    class Meta:
        model = DivanCategory
        fields = ['group_name','little_group_name','text_content']

