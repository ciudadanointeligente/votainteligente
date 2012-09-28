from django.contrib import admin
from models import *

class IndiceInline(admin.TabularInline):
    model = Indice

class CandidatoInline(admin.TabularInline):
    model = Candidato

class PreguntaInline(admin.TabularInline):
	model = Pregunta
      
class ComunaAdmin(admin.ModelAdmin):
	inlines = [
		CandidatoInline,
        IndiceInline
    ]
admin.site.register(Comuna, ComunaAdmin)

class PreguntaAdmin(admin.ModelAdmin):
	inlines = [
		CandidatoInline
	]
	model = Pregunta
admin.site.register(Pregunta, PreguntaAdmin)

class AreaAdmin(admin.ModelAdmin):
	pass

admin.site.register(Area, AreaAdmin)


class DatoAdmin(admin.ModelAdmin):
	pass

admin.site.register(Dato, DatoAdmin)





