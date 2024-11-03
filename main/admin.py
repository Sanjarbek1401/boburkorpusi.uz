from django.contrib import admin
from .models import AuthorInfo, Baburnoma, DivanCategory, DivanGroup, DivanLittleGroup,DivanText, AdminContact

admin.site.register(AuthorInfo)
admin.site.register(Baburnoma)
admin.site.register(DivanCategory)
admin.site.register(DivanGroup)
admin.site.register(DivanText)
admin.site.register(DivanLittleGroup)
admin.site.register(AdminContact)
