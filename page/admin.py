from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Firma,Sube,Icmal,FirmaIcmal,Donem


admin.site.register(Icmal)
admin.site.register(FirmaIcmal)
admin.site.register(Donem)




class FirmaResource(resources.ModelResource):
    class Meta:
        model = Firma
        fields =('id','isim','slug')
        export_order = ('id','isim','slug')


class FirmaAdmin(ImportExportModelAdmin):
    resource_classes = [FirmaResource]

admin.site.register(Firma, FirmaAdmin)

class SubeResource(resources.ModelResource):
    class Meta:
        model = Sube
        fields =('id','isim','firma','slug','sgkNo')
        export_order = ('id','isim','firma','slug','sgkNo' )


class SubeAdmin(ImportExportModelAdmin):
    resource_classes = [SubeResource]

admin.site.register(Sube, SubeAdmin)