
from django.contrib import admin
from django.urls import path
from page.views import (home,createFirma,createSube,
                        createGirdi,firmaIcmalleri,grupIcmalleri,
                        subeIcmalleri,icmal_detay,firma_icmal_detay,
                        musteri_sunum_icmali,firma_musteri_sunum_icmali,
                        ayarlar,icmallerim,generatePdf,generatePdfFirma,generatePdfGrup,signinView,signoutView,
                        signupView,profile,allSubeler,editSube,allFirmalar,editFirma,deleteSube,deleteFirma,
                        hizliBir,hizliIki,icmalGir,odemeIcmali,odemeIcmali2,OdemeIcmaliDevam,odemeTakipBir,odemeTakipIki
                        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('firmalar/<str:firma_slug>/', firmaIcmalleri, name='firmaIcmalleri'),
    path('gruplar/<str:grup_slug>/', grupIcmalleri, name='grupIcmalleri'),
    path('subeler/<str:firma_slug>/<str:sube_slug>/', subeIcmalleri, name='subeIcmalleri'),
    path('sube-icmal/<str:firma_slug>/<str:sube_slug>/<int:yil>/<int:ay>/', icmal_detay, name='icmal_detay'),
    path('firma-icmal/<str:firma_slug>/<int:yil>/<int:ay>/', firma_icmal_detay, name='firma_icmal_detay'),
    path('sube-muster-sunum/<str:firma_slug>/<str:sube_slug>/<int:yil>/<int:ay>/', musteri_sunum_icmali, name='musteri_sunum_icmali'),
    path('firma-muster-sunum/<str:firma_slug>/<int:yil>/<int:ay>/', firma_musteri_sunum_icmali, name='firma_musteri_sunum_icmali'),
    path('firma/olustur/', createFirma, name='createFirma'),
    path('sube/olustur/', createSube, name='createSube'),
    path('icmal/olustur/', createGirdi, name='createGirdi'),
    path('icmal/olustur/<str:firma_slug>/<str:sube_slug>/', icmalGir, name='icmalGir'),
    path('ayarlar/', ayarlar, name='ayarlar'),
    path('icmallerim/', icmallerim, name='icmallerim'),
    path('pdf/sube/<str:firma_slug>/<str:sube_slug>/<int:yil>/<int:ay>/', generatePdf, name='generatePdf'),
    path('pdf/firma/<str:firma_slug>/<int:yil>/<int:ay>/', generatePdfFirma, name='generatePdfFirma'),
    path('pdf/grup/<int:yil>/<int:ay>/', generatePdfGrup, name='generatePdfGrup'),
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
    path("odeme-icmali/olustur/", odemeIcmali, name="odemeIcmali"),
    path("odeme-icmali/", odemeIcmali2, name="odemeIcmali2"),
    path("odeme-icmali/<int:satır_sayisi>/", OdemeIcmaliDevam, name="OdemeIcmaliDevam"),
    path("odeme-takip/", odemeTakipBir, name="odemeTakipBir"),
    path("odeme-takip/<int:yil>/<int:ay>/", odemeTakipIki, name="odemeTakipIki"),
]
