from django.template.loader import get_template
from .utils import render_to_pdf

from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import Firma,Icmal,Sube,FirmaIcmal,YEAR_CHOICES,MONTH_CHOICES,GrupIcmal
from .forms import FirmaForm,SubeForm,GirdiForm,SignInForm,SignUpForm,FirmaCreateForm,HizliForm,IcmalBir,OdemeIcmaliForm,IcmalUc


def generatePdf(request,firma_slug,sube_slug,ay,yil):
    pdf = render_to_pdf('mytemplate.html',firma_slug=firma_slug,sube_slug=sube_slug,ay=ay,yil=yil)
    return HttpResponse(pdf, content_type='application/pdf')


def generatePdfFirma(request,firma_slug,ay,yil):
    pdf = render_to_pdf('mytemplate.html',firma_slug=firma_slug,ay=ay,yil=yil)
    return HttpResponse(pdf, content_type='application/pdf')


def generatePdfGrup(request,ay,yil):
    pdf = render_to_pdf('mytemplate.html',grup_slug=True,ay=ay,yil=yil)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def hizliBir(request):
    context = dict()
    context['title'] = "Şubelere SGK Gir"
    context['form'] = HizliForm(request.POST)
    if request.method == "POST":
        if context['form'].is_valid():
            firma = context['form'].cleaned_data['firma']
            return redirect("hizliIki", firma_slug=firma.slug)
    return render(request,"hizli-1.html",context)


@login_required
def hizliIki(request,firma_slug):
    context = dict()
    context['title'] = "Şubelere SGK Gir"
    firma = Firma.objects.get(slug=firma_slug)
    icmaller = Icmal.objects.filter(firma=firma,yıl=YEAR_CHOICES[0][0],ay=MONTH_CHOICES[0][0])
    context['subeIcmalleri'] = icmaller
    context['firma'] = firma
    SgkFormSet = modelformset_factory(Icmal, fields=['sgk', 'tesvik'])
    queryset = icmaller
    context["sayi"] = len(icmaller)
    if request.method == "POST":
        context['formset'] = SgkFormSet(
            request.POST, request.FILES,
            queryset=queryset
        )
        if context['formset'].is_valid():
            context['formset'].save()
            messages.success(request,'Giriş Başarıyla Kaydedildi.')
            
        else:
            messages.info(request,'Kaydedilemedi.')
        return redirect("hizliIki", firma_slug=firma_slug)
    else:
        context['formset'] = SgkFormSet(queryset=queryset)
    return render(request,'hizli-3.html',context)


@login_required
def home(request):
    context=dict()
    items = GrupIcmal.objects.all()
    for item in items:
        item.delete()
    context['title'] = "Anasayfa"
    context['firma_sayisi'] = len(Firma.objects.all())
    context['sube_sayisi'] = len(Sube.objects.all())
    context['kullanici_sayisi'] = len(User.objects.all())
    return render(request,'home.html',context)


@login_required
def createFirma(request):
    context = dict()
    context['title'] = "Firma Oluştur"
    context['form'] = FirmaCreateForm(request.POST)
    if request.method == 'POST':
        if context['form'].is_valid():
            isim = context['form'].cleaned_data['isim']
            sube = context['form'].cleaned_data['sube']
            sgk = context['form'].cleaned_data['sgkNo']
            firma = Firma(isim=isim)
            firma.save()
            sube= Sube(isim=sube,sgkNo=sgk,firma=firma,merkez=True)           
            sube.save()
            messages.success(request,'Firma ve Merkez Şubesi Başarıyla Oluşturuldu.')
            return redirect('ayarlar')
        else:
            messages.info(request,'Firma ismi hatalı..')
            return redirect('createFirma')   
    return render(request,'firma-form.html',context)

@login_required
def editFirma(request,firma_slug):
    context = dict()
    context['title'] = "Firma Düzenle"
    firma = Firma.objects.get(slug=firma_slug)
    context['form'] = FirmaForm(instance=firma)
    if request.method == 'POST':
        context['form'] = FirmaForm(request.POST,instance=firma)
        if context['form'].is_valid():
            item = context['form'].save(commit=False)
            item.save()
            messages.success(request,'Firma Başarıyla Kaydedildi.')
            return redirect('ayarlar')
        else:
            messages.info(request,'Firma ismi hatalı..')
    return render(request,'firma-form.html',context)

@login_required
def deleteFirma(request,firma_slug):
    firma = Firma.objects.get(slug=firma_slug)
    firma.delete()
    messages.success(request,'Firma Başarıyla Silindi')
    return redirect("allFirmalar")

@login_required
def createSube(request):
    context = dict()
    context['title'] = "Şube Oluştur"
    context['form'] = SubeForm(request.POST)
    if request.method == 'POST':
        if context['form'].is_valid():
            context['form'].save()
            messages.success(request,'Şube Başarıyla Oluşturuldu.')
            return redirect('ayarlar')
        else:
            messages.info(request,'Şube ismi hatalı...')
            return redirect(createSube)   
    return render(request,'sube-form.html',context)

@login_required
def editSube(request,firma_slug,sube_slug):
    context = dict()
    context['title'] = "Şube Düzenle"
    firma = Firma.objects.get(slug=firma_slug)
    sube = Sube.objects.get(slug=sube_slug,firma=firma)
    context['form'] = SubeForm(instance=sube)
    if request.method == 'POST':
        context['form'] = SubeForm(request.POST,instance=sube)
        if context['form'].is_valid():
            item = context['form'].save(commit=False)
            item.save()
            messages.success(request,'Şube Başarıyla Kaydedildi.')
            return redirect('ayarlar')
        else:
            messages.info(request,'Şube ismi hatalı...')
    return render(request,'sube-form.html',context)

@login_required
def deleteSube(request,firma_slug,sube_slug):
    firma = Firma.objects.get(slug=firma_slug)
    sube = Sube.objects.get(slug=sube_slug,firma=firma)
    sube.delete()
    messages.success(request,'Şube Başarıyla Silindi')
    return redirect("allSubeler")
    

@login_required
def createGirdi(request):
    context = dict()
    context['title'] = "İcmal Girişi - Firma Seçin"
    context['subeForm'] = IcmalBir(request.POST)
    if request.method == 'POST':
        if context['subeForm'].is_valid():
            sube = context['subeForm'].cleaned_data['sube']
            firma = sube
            subeler = Sube.objects.filter(firma=firma)
            merkez_sube = ""
            for sube in subeler:
                if sube.merkez:
                    merkez_sube = sube
            return redirect("icmalGir", firma_slug=firma.slug, sube_slug = merkez_sube.slug)
    return render(request,'girdi-form.html',context)


@login_required
def icmalGir(request,firma_slug,sube_slug):
    context = dict()
    context['title'] = "İcmal Girişi"
    firma = Firma.objects.get(slug = firma_slug)
    sube = Sube.objects.get(firma=firma, slug = sube_slug)
    icmal = Icmal.objects.get(firma=firma,sube=sube)
    context['form'] = GirdiForm(instance=icmal)
    context['subeForm'] = IcmalUc(request.POST)
    if request.method == "POST":
        if  'icmal-getir' in request.POST :   
            if context['subeForm'].is_valid():
                sube = context['subeForm'].cleaned_data['sube']
                firma = sube.firma
                return redirect("icmalGir", firma_slug=firma.slug, sube_slug = sube.slug)
        if 'icmal-kaydet' in request.POST:  
            context['form'] = GirdiForm(request.POST,instance=icmal)   
            if context['form'].is_valid():
                item = context['form'].save(commit=False)
                item.save()
                messages.success(request,'İcmal Başarıyla Kaydedildi')
                return redirect("icmalGir", firma_slug=firma.slug, sube_slug = sube.slug)
    return render(request,'girdi-form.html',context)


@login_required
def odemeIcmali(request):
    context = dict()
    items = GrupIcmal.objects.all()
    for item in items:
        item.delete()
    context['title'] = "Ödeme İcmali Oluştur"
    context['form'] = OdemeIcmaliForm(request.POST)
    if request.method == 'POST':
        if context['form'].is_valid():
            satır_sayisi = context['form'].cleaned_data['satır']
            return redirect("OdemeIcmaliDevam", satır_sayisi=satır_sayisi)
    return render(request,'odeme-icmali-form.html', context)


@login_required
def OdemeIcmaliDevam(request,satır_sayisi):
    context = dict()
    context['title'] = "Ödeme İcmali Oluştur-2"
    context['form'] = OdemeIcmaliForm(request.POST)
    if request.method == 'POST':
        if context['form'].is_valid():
            satır_sayisi = context['form'].cleaned_data['satır']
            return redirect("OdemeIcmaliDevam", satır_sayisi=satır_sayisi)
    context['satir'] = range(1,satır_sayisi+1)
    context['sayi'] = satır_sayisi
    context['icmaller'] = Icmal.objects.filter(ay=MONTH_CHOICES[0][0], yıl=YEAR_CHOICES[0][0])
    return render(request,'odeme-icmali-form.html',context)


@login_required
def odemeIcmali2(request):
    context = dict()
    satir = int(request.POST.getlist('satir_sayisi')[0])
    count=1
    i = 0
    subeler =list()
    while i < satir:
        subeler.append(request.POST.getlist('secilenler_{}'.format(count)))
        i +=1
        count+=1
    for index,kutu in enumerate(subeler):
        listem = list()
        for i in kutu:
            icmal = Icmal.objects.get(pk=i)
            listem.append(icmal)
        print(listem)
        try:
            a = GrupIcmal.objects.get(baslik=request.POST.getlist('secilen_baslik_{}'.format(index+1))[0],ay=MONTH_CHOICES[0][0], yıl=YEAR_CHOICES[0][0])
        except:
            a = GrupIcmal(baslik=request.POST.getlist('secilen_baslik_{}'.format(index+1))[0],ay=MONTH_CHOICES[0][0], yıl=YEAR_CHOICES[0][0])
            atak =0
            yasalKdv =0 
            tasdik = 0
            kdv =0
            kdv2 = 0
            muhtasar = 0
            ggkv = 0
            damga =0
            mtv =0
            ceza =0
            idariceza = 0
            davagideri =0
            hakemheyeti =0
            geçmişborçlar =0
            tesvik=0
            müsavirlik=0
            harcama=0
            sgk=0
            bagkur=0
            for icmal in listem:
                atak += icmal.atak
                yasalKdv += icmal.yasalKdv
                tasdik += icmal.tasdik
                kdv += icmal.kdv
                kdv2 += icmal.kdv2
                muhtasar += icmal.muhtasar
                ggkv += icmal.ggkv
                damga += icmal.damga
                mtv += icmal.mtv
                ceza += icmal.ceza
                idariceza += icmal.idariceza
                davagideri += icmal.davagideri
                hakemheyeti += icmal.hakemheyeti
                geçmişborçlar += icmal.geçmişborçlar
                tesvik += icmal.tesvik
                müsavirlik += icmal.müsavirlik
                harcama += icmal.harcama
                sgk += icmal.sgk
                bagkur += icmal.bagkur
            a.atak = atak
            a.yasalKdv = yasalKdv
            a.tasdik = tasdik
            a.kdv = kdv
            a.kdv2 = kdv2
            a.muhtasar = muhtasar
            a.ggkv = ggkv
            a.damga = damga
            a.mtv = mtv
            a.ceza = ceza
            a.idariceza = idariceza
            a.davagideri = davagideri
            a.hakemheyeti = hakemheyeti
            a.geçmişborçlar = geçmişborçlar
            a.tesvik = tesvik
            a.müsavirlik = müsavirlik
            a.harcama = harcama
            a.sgk = sgk
            a.bagkur = bagkur
            a.save()
            
    context['items'] = GrupIcmal.objects.all()
    context['yıl'] =YEAR_CHOICES[0][0]
    context['ay'] =MONTH_CHOICES[0][0]
    return render(request,'grup-table.html',context)

@login_required
def firmaIcmalleri(request,firma_slug):
    context =dict()
    context['title'] ="Firma İcmal Listesi"
    firma = Firma.objects.get(slug=firma_slug)
    context['firma'] = firma
    context['icmaller'] = FirmaIcmal.objects.filter(firma=firma)
    return render(request,'icmal-list.html',context)

@login_required
def grupIcmalleri(request,grup_slug):
    pass

@login_required
def allSubeler(request):
    context =dict()
    context['title'] = "Tüm Şubeler"
    return render(request,'sube-table.html',context)

@login_required
def allFirmalar(request):
    context =dict()
    context['title'] = "Tüm Firmalar"
    return render(request,'firma-table.html',context)

@login_required
def subeIcmalleri(request,sube_slug,firma_slug):
    context = dict()
    firma = Firma.objects.get(slug=firma_slug)
    sube = Sube.objects.get(slug=sube_slug,firma=firma)
    context['title'] = "Şube İcmal Listesi"
    context['sube'] = sube
    context['icmaller'] = Icmal.objects.filter(sube=sube)
    return render(request,'icmal-list.html',context)

@login_required
def icmal_detay(request,firma_slug,sube_slug,yil,ay):
    context = dict()
    context['title'] = "Şube İcmal Detayı"
    firma = Firma.objects.get(slug=firma_slug)
    sube = Sube.objects.get(slug=sube_slug,firma=firma)
    context['sube'] = sube
    icmal = Icmal.objects.get(sube=sube,yıl=yil,ay=ay)
    context['icmal'] = icmal
    return render(request,'icmal-detail.html',context)

@login_required
def musteri_sunum_icmali(request,firma_slug,sube_slug,yil,ay):
    context = dict()
    context['title'] = "Şube Müşteri Sunum İcmali"
    firma = Firma.objects.get(slug=firma_slug)
    sube = Sube.objects.get(slug=sube_slug,firma=firma)
    context['sube'] = sube
    icmal = Icmal.objects.get(sube=sube,yıl=yil,ay=ay)
    context['icmal'] = icmal
    context['firma'] = firma
    return render(request,'musteri-sunum.html',context)

@login_required
def firma_musteri_sunum_icmali(request,firma_slug,yil,ay):
    context = dict()
    context['title'] = "Firma Müşteri Sunum İcmali"
    firma = Firma.objects.get(slug=firma_slug)
    context['subeler'] = Sube.objects.filter(firma=firma)
    subeIcmalleri = []
    for sube in context['subeler']:
        try:
            i = Icmal.objects.get(sube=sube)
            subeIcmalleri.append(i)
        except:
            continue
    context['subeIcmalleri'] = subeIcmalleri
    icmal = FirmaIcmal.objects.get(firma=firma,yıl=yil,ay=ay)
    context['icmal'] = icmal
    return render(request,'musteri-sunum.html',context)


@login_required
def firma_icmal_detay(request,firma_slug,yil,ay):
    context = dict()
    context['title'] = "Firma İcmal Detayı"
    firma = Firma.objects.get(slug=firma_slug)
    context['subeler'] = Sube.objects.filter(firma=firma)
    subeIcmalleri = []
    for sube in context['subeler']:
        try:
            i = Icmal.objects.get(sube=sube)
            subeIcmalleri.append(i)
        except:
            continue
    context['subeIcmalleri'] = subeIcmalleri
    icmal = FirmaIcmal.objects.get(firma=firma,yıl=yil,ay=ay)
    context['icmal'] = icmal
    return render(request,'icmal-detail.html',context)




@login_required
def ayarlar(request):
    context = dict()
    context['title'] = "Ayarlar"
    return render(request,'ayarlar.html',context)


@login_required
def icmallerim(request):
    context = dict()
    context['title'] = "İcmallerim"
    user = request.user
    context['icmaller'] = Girdi.objects.filter(personel=user)
    return render(request,"icmallerim.html",context)


@login_required
def signupView(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kaydınız başarıyla oluşturuldu. Giriş yapabilirsiniz.')
            return redirect('ayarlar')
        else:
            messages.info(request,'Şifreniz tamamen sayısal veya 8 haneden kısa olmamalıdır.')
    else:
        form = SignUpForm()
    return render(request, 'signin-form.html',{'form':form,'title' : 'Kullanıcı Oluştur'})



def signinView(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request,'Hesabınız Engellendi')
            else:
                messages.info(request,'Yanlış kullanıcı adı veya şifre')
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form':form})



def signoutView(request):
    logout(request)
    return redirect('home')



@login_required
def profile(request):
    context = dict()
    context['title'] = 'Profili Düzenle'
    user = request.user
    context['form'] = SignUpForm(instance=user)
    if request.method == "POST":
        context['form'] = SignUpForm(request.POST,instance=user)
        if context['form'].is_valid():
            item = context['form'].save(commit=False)
            item.save()
            messages.success(request,'Değişiklikler Kaydedildi.')
    return render(request,'signin-form.html',context)


@login_required
def noname(request):
    context=dict()
    return
