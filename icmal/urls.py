
from django.contrib import admin
from django.urls import path
from page.views import (home,createFirma,createSube,
                        createGirdi,firmaIcmalleri,
                        firma_musteri_sunum_icmali,
                        ayarlar,generatePdf,generatePdfFirma,generatePdfGrup,signinView,signoutView,
                        signupView,profile,allSubeler,editSube,allFirmalar,editFirma,deleteSube,deleteFirma,
                        hizliBir,hizliIki,icmalGir,odemeTakip,
                        generatePdfOdemeTakip
                        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('firmalar/<str:firma_slug>/', firmaIcmalleri, name='firmaIcmalleri'),
    path('firma-muster-sunum/<str:firma_slug>/<int:yil>/<int:ay>/', firma_musteri_sunum_icmali, name='firma_musteri_sunum_icmali'),
    path('firma/olustur/', createFirma, name='createFirma'),
    path('sube/olustur/', createSube, name='createSube'),
    path('icmal/olustur/', createGirdi, name='createGirdi'),
    path('icmal/olustur/<str:firma_slug>/<str:sube_slug>/', icmalGir, name='icmalGir'),
    path('ayarlar/', ayarlar, name='ayarlar'),
    path('pdf/sube/<str:firma_slug>/<str:sube_slug>/<int:yil>/<int:ay>/', generatePdf, name='generatePdf'),
    path('pdf/firma/<str:firma_slug>/<int:yil>/<int:ay>/', generatePdfFirma, name='generatePdfFirma'),
    path('pdf/grup/<int:yil>/<int:ay>/', generatePdfGrup, name='generatePdfGrup'),
    path('pdf/odeme-takip/<int:yil>/<int:ay>/',generatePdfOdemeTakip, name="generatePdfOdemeTakip" ),
    path('login/', signinView, name='signinView'),
    path('logout/', signoutView, name='signoutView'),
    path('signup/', signupView, name='signupView'),
    path('profile/', profile, name='profile'),
    path('subeler/', allSubeler, name='allSubeler'),
    path('firmalar/', allFirmalar, name='allFirmalar'),
    path("sube/duzenle/<str:firma_slug>/<str:sube_slug>/", editSube, name="editSube"),
    path("firma/duzenle/<str:firma_slug>/", editFirma ,name="editFirma"),
    path("sil/sube/<str:firma_slug>/<str:sube_slug>/", deleteSube, name="deleteSube"),
    path("sil/firma/<str:firma_slug>/", deleteFirma, name="deleteFirma"),
    path("hizli-sgk-1/", hizliBir, name="hizliBir"),
    path("hizli-sgk/<str:firma_slug>/", hizliIki, name="hizliIki"),
    path("odeme-takip/", odemeTakip, name="odemeTakip"),

]
