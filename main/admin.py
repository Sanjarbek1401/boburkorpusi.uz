from django.contrib import admin
from .models import DevonCategory, DevonGroup, DevonText, Baburnoma,  DevonItem, Work, Dictionary
from django.db import models
from django.forms import Textarea


@admin.register(DevonCategory)
class DevonCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'count', 'order']
    list_editable = ['count', 'order']
    search_fields = ['name']
    ordering = ('order',)

@admin.register(DevonGroup)
class DevonGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_filter = ['category']
    list_editable = ['order']
    search_fields = ['name']
    ordering = ('order',)

@admin.register(DevonText)
class DevonTextAdmin(admin.ModelAdmin):
    list_display = ['group', 'text', 'order']
    list_filter = ['group__category', 'group']
    list_editable = ['order']
    search_fields = ['text']
    ordering = ('order',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
    }

@admin.register(Baburnoma)
class BaburnomaAdmin(admin.ModelAdmin):
    list_display = ['title', 'has_pdf', 'has_text', 'uploaded_at']
    search_fields = ['title', 'text_content']
    readonly_fields = ['uploaded_at']
    ordering = ('-uploaded_at',)
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 30, 'cols': 100})},
    }
    
    fieldsets = (
        ('Asosiy', {
            'fields': ('title', 'pdf_file'),
        }),
        ('Qidiruv uchun matn', {
            'fields': ('text_content',),
            'description': 'Bu yerga Boburnoma matnini qidiruvda ishlashi uchun joylashtiring. Bu matn faqat qidiruv uchun ishlatiladi.',
        }),
        ('Qo\'shimcha', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',),
        }),
    )

    def has_pdf(self, obj):
        return bool(obj.pdf_file)
    has_pdf.short_description = 'PDF mavjud'
    has_pdf.boolean = True

    def has_text(self, obj):
        return bool(obj.text_content)
    has_text.short_description = 'Matn mavjud'
    has_text.boolean = True



@admin.register(DevonItem)
class DevonItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order']
    list_editable = ['order']
    list_filter = ['category']
    search_fields = ['title', 'content']
    ordering = ('order',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
    }

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order']
    list_editable = ['order']
    list_filter = ['category']
    search_fields = ['title', 'content']
    ordering = ('order',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
    }

@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('word', 'description')
    search_fields = ('word', 'description')
    ordering = ('word',)
    list_per_page = 20
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
    }
    fieldsets = (
        (None, {
            'fields': ('word', 'description')
        }),
    )