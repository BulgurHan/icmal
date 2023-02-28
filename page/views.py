
from .utils import render_to_pdf,save_as_zip
import datetime
import xlwt
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import FileResponse
from django.shortcuts import render,redirect,HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import Firma,Icmal,Sube,FirmaIcmal,Donem
from .forms import FirmaForm,SubeForm,GirdiForm,SignInForm,SignUpForm,FirmaCreateForm,HizliForm,IcmalBir,IcmalUc,DonemForm,KullaniciDonemForm



def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="odeme_icmali.xls"'
    donem = Donem.objects.get(kullanici=request.user)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('İcmal')
    # Write header row
    row_num = 0
    columns = ['', '', '','', '','','','','']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)


    sube_data = Icmal.objects.filter(ay=donem.ay,yıl=donem.yil)
    firma_data = FirmaIcmal.objects.filter(ay=donem.ay,yıl=donem.yil)
    for firma in firma_data:
        row_num += 1
        columns = [firma.firma.isim, 'KDV', 'Muhtasar','Diğer Vergi ve Cezalar','Atak Fatura', 'Yasal KDV','Gelir/Geçici Kurumlar Vergisi','Defter Açılış-Kapanış Tasdik Ücreti','Trafik Cezaları ve MTV','Vergi Yapılandırması','SGK Yapılandırması' ,'Geçmiş Aylarda Ödenmeyen Vergi ve Borçlar','Toplam','Bağkur','Toplam','Muhasebe','Teşvik','Toplam','SGK','Toplam']
        for col_num, column_title in enumerate(columns):
            col_style = xlwt.easyxf('font: bold 1')
            ws.write(row_num, col_num, column_title,col_style)
        
        for sube in sube_data:
            if sube.sube.firma == firma.firma:
                row_num += 1
                row = [sube.sube.isim, sube.kdvler,sube.muhtasar,sube.yargı_dava_ceza,sube.atak,sube.yasalKdv,sube.ggkv,sube.tasdik,sube.ceza,sube.vergiYapilandirmasi,sube.sgkYapilandirmasi,sube.geçmişborçlar,sube.uclutoplam,sube.bagkur,sube.dortlutoplam,sube.müsavirlik,sube.tesvik,sube.beslitoplam,sube.sgk,sube.altilitoplam]
                for col_num, cell_value in enumerate(row):
                    ws.write(row_num, col_num, cell_value)
        
        row_num += 1
        columns = ['TOPLAM', firma.kdvler, firma.muhtasar,firma.yargı_dava_ceza,firma.atak,firma.yasalKdv,firma.ggkv,firma.tasdik,firma.ceza,firma.vergiYapilandirmasi,firma.sgkYapilandirmasi,firma.geçmişborçlar,firma.uclutoplam,firma.bagkur,firma.dortlutoplam,firma.müsavirlik,firma.tesvik,firma.beslitoplam,firma.sgk,firma.altilitoplam]
        for col_num, column_title in enumerate(columns):
            col_style = xlwt.easyxf('font: bold 1')
            ws.write(row_num, col_num, column_title,col_style)

    wb.save(response)
    return response


def generatePdf(request,firma_slug,sube_slug,ay,yil):
    firma = Firma.objects.get(slug=firma_slug)
    sube = Sube.objects.get(firma=firma,slug=sube_slug)
    response = render_to_pdf('mytemplate.html',firma_slug=firma_slug,sube_slug=sube_slug,ay=ay,yil=yil)
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(str(sube.slug))
    return response

    


def generatePdfFirma(request,firma_slug,ay,yil):
    firma = Firma.objects.get(slug=firma_slug)
    response = render_to_pdf('mytemplate.html',firma_slug=firma_slug,ay=ay,yil=yil)
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(str(firma.slug))
    return response



def generatePdfOdemeTakip(request):
    template_path = 'pdf.html'
    context = {'my_data': 'Lorem ipsum'}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="my_pdf.pdf"'
    template = get_template(template_path)
    html = template.render(context, request)
    pisa.CreatePDF(html, response)
    return response


def tektuslaPDF(request,firma_slug,ay,yil):
    firma = Firma.objects.get(slug=firma_slug)
    subeler = Sube.objects.filter(firma=firma)
    pdfListesi = []
    for sube in subeler:
        pdfListesi.append(generatePdf(request,firma_slug=firma_slug,sube_slug=sube.slug,ay=ay,yil=yil))
    save_as_zip(pdfListesi,subeler)
    file = open('responses.zip', 'rb')
    response = FileResponse(file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={}.zip'.format(str(firma_slug))
    return response
    
        
    

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
    donem = Donem.objects.get(kullanici=request.user)
    icmaller = Icmal.objects.filter(firma=firma,yıl=donem.yil,ay=donem.ay)
    if len(icmaller) == 0:
        subeler = Sube.objects.filter(firma=firma)
        for sube in subeler:
            a = Icmal(firma=firma,sube=sube,ay=donem.ay,yıl=donem.yil)
            a.save()
    icmaller = Icmal.objects.filter(firma=firma,yıl=donem.yil,ay=donem.ay)
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
    #dev code 

    # icmaller = Icmal.objects.all()
    # for icmal in icmaller:
    #     icmal.save()
    # firmaicmalleri = FirmaIcmal.objects.all()
    # for firmaicmal in firmaicmalleri:
    #     firmaicmal.save()
        
    try:
        donem = Donem.objects.get(kullanici=request.user)
    except:
        donem = Donem(kullanici=request.user,ay=datetime.datetime.now().month,yil=datetime.datetime.now().year)
        donem.save()
    context['donem'] = donem
    context['form'] = KullaniciDonemForm(instance=donem) 
    context['title'] = "Anasayfa"
    context['firma_sayisi'] = len(Firma.objects.all())
    context['sube_sayisi'] = len(Sube.objects.all())
    context['kullanici_sayisi'] = len(User.objects.all())
    if request.method == "POST":
        context['form'] = KullaniciDonemForm(request.POST,instance=donem)
        if context['form'].is_valid():
            item = context['form'].save(commit=False)
            item.kullanici = request.user
            item.save()
            messages.info(request,"Döneminiz Başarıyla Güncellendi")
            return redirect("home")
        else:
            messages.info(request,"Ops.")
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
    context['fslug'] = firma.slug
    context['selected']=sube
    context['subeler'] = Sube.objects.filter(firma=firma).order_by("isim")
    subeler = list(context['subeler'])
    i = subeler.index(sube)
    j=0
    for index,s in enumerate(subeler):
        if i == index:
            j = i+1
    try:
        sıradaki = subeler[j]
        context['slug'] = sıradaki.slug
    except:
        sıradaki = subeler[0]
        context['slug'] = sıradaki.slug
    donem = Donem.objects.get(kullanici=request.user)
    try:
        icmal = Icmal.objects.get(firma=firma,sube=sube,ay=donem.ay,yıl=donem.yil)
    except:
        icmal = Icmal(firma=firma,sube=sube,ay=donem.ay,yıl=donem.yil)
        icmal.save()
    context['form'] = GirdiForm(instance=icmal)
    if request.method == "POST":
        if  'icmal-getir' in request.POST :   
            sube =Sube.objects.get(isim=request.POST['sube'],firma=firma)
            return redirect("icmalGir", firma_slug=firma.slug, sube_slug = sube.slug)
        if 'icmal-kaydet' in request.POST:  
            context['form'] = GirdiForm(request.POST,instance=icmal)   
            if context['form'].is_valid():
                item = context['form'].save(commit=False)
                item.save()
                messages.success(request,'İcmal Başarıyla Kaydedildi')
                return redirect("icmalGir", firma_slug=firma.slug, sube_slug = sube.slug)
            else:
                print(context['form'].errors)
    return render(request,'girdi-form.html',context)



@login_required
def firmaIcmalleri(request,firma_slug):
    context =dict()
    context['title'] ="Firma İcmal Listesi"
    firma = Firma.objects.get(slug=firma_slug)
    donem = Donem.objects.get(kullanici=request.user)
    context['firma'] = firma
    context['icmaller'] = FirmaIcmal.objects.filter(firma=firma,ay=donem.ay,yıl=donem.yil)
    return render(request,'icmal-list.html',context)



@login_required
def allSubeler(request):
    context =dict()
    context['title'] = "Tüm Şubeler"
    context['subeler'] = Sube.objects.all()
    return render(request,'sube-table.html',context)

@login_required
def allFirmalar(request):
    context =dict()
    context['title'] = "Tüm Firmalar"
    return render(request,'firma-table.html',context)

@login_required
def allKullanicilar(request):
    context =dict()
    context['title'] = "Tüm Kullanıcılar"
    context['users'] = User.objects.all()
    return render(request,'user-table.html',context)

@login_required
def yetkiVer(request,username):
    kullanici = User.objects.get(username=username)
    if kullanici.is_superuser:
        kullanici.is_superuser = False
    else:
        kullanici.is_superuser = True
    messages.success(request, 'Kullanıcı başarıyla güncellendi')
    kullanici.save()
    return redirect('allKullanicilar')

@login_required
def kullaniciSil(request,username):
    kullanici = User.objects.get(username=username)
    kullanici.delete()
    messages.success(request, 'Kullanıcı başarıyla silindi')
    return redirect('allKullanicilar')


@login_required
def firma_musteri_sunum_icmali(request,firma_slug,yil,ay):
    context = dict()
    context['title'] = "Firma Müşteri Sunum İcmali"
    firma = Firma.objects.get(slug=firma_slug)
    context['subeler'] = Sube.objects.filter(firma=firma)
    subeIcmalleri = []
    for sube in context['subeler']:
        try:
            i = Icmal.objects.get(sube=sube,ay=ay,yıl=yil)
            subeIcmalleri.append(i)
        except:
            continue
    context['subeIcmalleri'] = subeIcmalleri
    icmal = FirmaIcmal.objects.get(firma=firma,yıl=yil,ay=ay)
    context['icmal'] = icmal
    return render(request,'musteri-sunum.html',context)



@login_required
def ayarlar(request):
    context = dict()
    context['title'] = "Ayarlar"
    return render(request,'ayarlar.html',context)




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
def odemeTakip(request):
    context=dict()
    donem = Donem.objects.get(kullanici=request.user)
    context["yil"] = donem.yil
    context["ay"] = donem.ay
    context['title']="Ödeme Takip İcmali"
    context['subeIcmalleri'] = Icmal.objects.filter(ay=donem.ay,yıl=donem.yil)
    context['firmaIcmalleri'] = FirmaIcmal.objects.filter(ay=donem.ay,yıl=donem.yil)
    return render(request,"odeme-takip2.html",context)



