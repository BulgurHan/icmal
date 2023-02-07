from django.contrib import admin
from .models import Firma,Sube,Icmal,FirmaIcmal,Donem


admin.site.register(Icmal)
admin.site.register(FirmaIcmal)
admin.site.register(Donem)



class SubeAdmin(admin.ModelAdmin):
    list_display = ['pk','isim','merkez']
    list_editable = ['isim', "merkez"]
    list_per_page = 20

admin.site.register(Sube,SubeAdmin)
admin.site.register(Firma)



