from django.contrib import admin
from models import *

class IndiceInline(admin.TabularInline):
    model = Indice
    
class ComunaAdmin(admin.ModelAdmin):
	inlines = [
        IndiceInline,
    ]

admin.site.register(Comuna, ComunaAdmin)


class AreaAdmin(admin.ModelAdmin):
	pass

admin.site.register(Area, AreaAdmin)


class DatoAdmin(admin.ModelAdmin):
	pass

admin.site.register(Dato, DatoAdmin)





