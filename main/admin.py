from django.contrib import admin
from .models import  DivanCategory, DivanGroup, DivanText, AdminContact,Baburnoma


@admin.register(DivanCategory)
class DivanCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','image']
    search_fields = ['name']

@admin.register(DivanGroup)
class DivanGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(DivanText)
class DivanTextAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text']

@admin.register(AdminContact)
class AdminContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','message','created_at']
    search_fields = ['name','email','message']

@admin.register(Baburnoma)
class BaburnomaAdmin(admin.ModelAdmin):
    list_display = ['title','description','uploaded_at']
    