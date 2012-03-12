from django.contrib import admin
from associates.models import Associate

class AssociateAdmin(admin.ModelAdmin):
    fieldsets = (
                (None, {'fields': ('name', 'slug', 'type', 'avatar', 'inner_circle')}),
                (None, {'fields': ('specialty', 'url', 'content',)})
            )

admin.site.register(Associate, AssociateAdmin)
