from rest_framework import serializers
from .models import AuthorInfo, Baburnoma, DivanCategory, DivanGroup, DivanText, AdminContact


class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorInfo
        fields = '__all__'


class BaburnomaSerializer(serializers.ModelSerializer):
    pdf_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Baburnoma
        fields = ['id', 'title',  'pdf_file', 'pdf_file_url', 'uploaded_at']

    def get_pdf_file_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None

class DivanTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivanText
        fields = ['id', 'text']


class DivanGroupSerializer(serializers.ModelSerializer):
    texts = DivanTextSerializer(many=True, read_only=True)

    class Meta:
        model = DivanGroup
        fields = ['id', 'name', 'category', 'texts']


class DivanCategorySerializer(serializers.ModelSerializer):
    groups = DivanGroupSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = DivanCategory
        fields = ['id', 'name', 'groups', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class AdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContact
        fields = '__all__'
