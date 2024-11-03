from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import DivanCategoryFilter
from .models import *
from .serializers import *
from drf_yasg import openapi


class AuthorInfoAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_description="Get author information")
    def get(self, request, *args, **kwargs):
        authors = AuthorInfo.objects.all()
        serializer = AuthorInfoSerializer(authors, many=True)
        return Response(serializer.data)


class BaburnomaAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        baburnoma = Baburnoma.objects.all()
        serializer = BaburnomaSerializer(baburnoma, many=True)
        return Response(serializer.data)


class DivanCategoryAPIView(APIView):
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DivanCategoryFilter
    search_fields = ['name', 'groups__name', 'groups__little_groups__name', 'groups__little_groups__texts__text']

    @swagger_auto_schema(
        operation_description="""
        List and search Divan categories.

        You can search using the following parameters:
        - group_name: Filter by Divan Group name
        - little_group_name: Filter by Divan Little Group name
        - text_content: Filter by text content
        - search: Search across all fields
        """,
        manual_parameters=[
            openapi.Parameter(
                'group_name',
                openapi.IN_QUERY,
                description="Filter by Divan Group name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'little_group_name',
                openapi.IN_QUERY,
                description="Filter by Divan Little Group name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'text_content',
                openapi.IN_QUERY,
                description="Filter by text content",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = DivanCategory.objects.prefetch_related(
            'groups',
            'groups__little_groups',
            'groups__little_groups__texts'
        ).distinct()
        serializer = DivanCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class DivanGroupAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        groups = DivanGroup.objects.all()
        serializer = DivanGroupSerializer(groups, many=True)
        return Response(serializer.data)


class DivanLittleGroupAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        little_groups = DivanLittleGroup.objects.all()
        serializer = DivanLittleGroupSerializer(little_groups, many=True)
        return Response(serializer.data)


class DivanTextAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        texts = DivanText.objects.all()
        serializer = DivanTextSerializer(texts, many=True)
        return Response(serializer.data)


class AdminContactAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        contacts = AdminContact.objects.all()
        serializer = AdminContactSerializer(contacts, many=True)
        return Response(serializer.data)
