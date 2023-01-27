import datetime
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



YEAR_CHOICES = []
MONTH_CHOICES = []

if datetime.datetime.now().month == 1:
    MONTH_CHOICES.append((12,12))
    YEAR_CHOICES.append((datetime.datetime.now().year-1,datetime.datetime.now().year-1))
elif datetime.datetime.now().month > 1:
    MONTH_CHOICES.append((datetime.datetime.now().month-1,datetime.datetime.now().month-1))
    YEAR_CHOICES.append((datetime.datetime.now().year,datetime.datetime.now().year))





class Firma(models.Model):
    isim = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,default="")
    def save(self, *args, **kwargs):        
        self.slug = slugify(self.isim)
        super(Firma, self).save(*args, **kwargs)
    def __str__(self):
        return self.isim





class Sube(models.Model):
    isim = models.CharField(max_length=250)
    firma = models.ForeignKey(Firma,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250,default="")
    merkez = models.BooleanField(default=False)
    sgkNo = models.CharField(max_length=26,null=True,blank=True)
    def save(self, *args, **kwargs):        
        self.slug = slugify(self.isim)
        super(Sube, self).save(*args, **kwargs)
    def __str__(self):
        return "{} Firması -{} Şubesi".format(self.firma.isim,self.isim)
    
    class Meta:
        ordering = ('firma__isim',)


@receiver(post_save, sender=Sube)
def icmal_olustur(sender, instance, created, **kwargs):
    if created:
        a = Icmal(sube=instance, yıl=YEAR_CHOICES[0][0], ay=MONTH_CHOICES[0][0])
        a.save()
        try:
            icmal = FirmaIcmal.objects.get(firma = instance.firma,yıl=YEAR_CHOICES[0][0], ay=MONTH_CHOICES[0][0])
        except:
            b = FirmaIcmal(firma=instance.firma,yıl=YEAR_CHOICES[0][0], ay=MONTH_CHOICES[0][0])       
            b.save()



   


class Icmal(models.Model):
    sube = models.ForeignKey(Sube,on_delete=models.CASCADE)
    firma = models.ForeignKey(Firma, null=True,blank=True, on_delete=models.CASCADE)
    yıl = models.IntegerField(('yıl'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    ay = models.IntegerField(('ay'), choices=MONTH_CHOICES, default=datetime.datetime.now().month)

    atak = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    yasalKdv = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    tasdik = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    kdv = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kdv2  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    muhtasar  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    ggkv  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    damga = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    mtv  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    ceza = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    idariceza  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    davagideri  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    hakemheyeti  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    geçmişborçlar  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    sgkYapilandirmasi = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    vergiYapilandirmasi = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)


    odemelertoplami = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    kdvler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    cezalar = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    digercezalar = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kosgebler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    müsavirlikler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)


    tesvik  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    müsavirlik  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    harcama  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    danismanliktoplami = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    
    sgk  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    bagkur  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    sgktoplamlari = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    toplam = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)


    def save(self, *args, **kwargs):        
        self.odemelertoplami =self.vergiYapilandirmasi+self.sgkYapilandirmasi+ self.kdv+self.kdv2+self.tasdik+self.muhtasar+self.ggkv+self.damga+self.mtv+self.ceza+self.idariceza+self.davagideri+self.hakemheyeti+self.geçmişborçlar+self.tesvik+self.müsavirlik+self.harcama+self.bagkur
        self.kdvler = self.kdv + self.kdv2
        self.toplam = self.odemelertoplami+self.sgk
        self.cezalar = self.ceza + self.mtv
        self.digercezalar = self.idariceza + self.davagideri + self.hakemheyeti
        self.müsavirlikler =self.müsavirlik + self.harcama
        self.firma = self.sube.firma
        super(Icmal, self).save(*args, **kwargs)
    def __str__(self):
        return "{}-{}".format(self.pk,self.sube.isim)

class FirmaIcmal(models.Model):
    firma = models.ForeignKey(Firma,on_delete=models.CASCADE)
    yıl = models.IntegerField(('yıl'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    ay = models.IntegerField(('ay'), choices=MONTH_CHOICES, default=datetime.datetime.now().month)
    atak = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    yasalKdv = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    tasdik = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kdv = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kdv2  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    muhtasar  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    ggkv  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    damga = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    mtv  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    ceza = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    idariceza  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    davagideri  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    hakemheyeti  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    geçmişborçlar  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    sgkYapilandirmasi = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    vergiYapilandirmasi = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    odemelertoplami = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    
    kdvler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    cezalar = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    digercezalar = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kosgebler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    müsavirlikler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    tesvik  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    müsavirlik  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    harcama  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    danismanliktoplami = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    
    sgk  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    bagkur  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    sgktoplamlari = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    toplam = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)


    def save(self, *args, **kwargs):        
        self.odemelertoplami =self.vergiYapilandirmasi+self.sgkYapilandirmasi+ self.kdv+self.kdv2+self.tasdik+self.muhtasar+self.ggkv+self.damga+self.mtv+self.ceza+self.idariceza+self.davagideri+self.hakemheyeti+self.geçmişborçlar+self.tesvik+self.müsavirlik+self.harcama+self.bagkur
        self.kdvler = self.kdv + self.kdv2
        self.toplam = self.odemelertoplami+self.sgk
        self.cezalar = self.ceza + self.mtv
        self.digercezalar = self.idariceza + self.davagideri + self.hakemheyeti
        self.müsavirlikler =self.müsavirlik + self.harcama
        super(FirmaIcmal, self).save(*args, **kwargs)


class GrupIcmal(models.Model):
    baslik = models.CharField(max_length=250)
    yıl = models.IntegerField(('yıl'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    ay = models.IntegerField(('ay'), choices=MONTH_CHOICES, default=datetime.datetime.now().month)
    atak = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    yasalKdv = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    tasdik = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kdv = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kdv2  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    muhtasar  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    ggkv  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    damga = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    mtv  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    ceza = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    idariceza  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    davagideri  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    hakemheyeti  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    geçmişborçlar  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    sgkYapilandirmasi = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    vergiYapilandirmasi = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    odemelertoplami = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    
    kdvler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    cezalar = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    digercezalar = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    kosgebler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    müsavirlikler = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    tesvik  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    müsavirlik  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    harcama  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    danismanliktoplami = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    
    sgk  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    bagkur  = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)
    sgktoplamlari = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)

    toplam = models.DecimalField(decimal_places=2, max_digits=11,null=True,default=0)


    def save(self, *args, **kwargs):        
        self.odemelertoplami =self.vergiYapilandirmasi+self.sgkYapilandirmasi+self.kdv+self.kdv2+self.tasdik+self.muhtasar+self.ggkv+self.damga+self.mtv+self.ceza+self.idariceza+self.davagideri+self.hakemheyeti+self.geçmişborçlar+self.tesvik+self.müsavirlik+self.harcama+self.bagkur
        self.kdvler = self.kdv + self.kdv2
        self.toplam = self.odemelertoplami+self.sgk
        self.cezalar = self.ceza + self.mtv
        self.digercezalar = self.idariceza + self.davagideri + self.hakemheyeti
        self.müsavirlikler =self.müsavirlik + self.harcama
        super(GrupIcmal, self).save(*args, **kwargs)
    def __str__(self):
        return self.baslik


@receiver(post_save, sender=Icmal)
def icmal_esitle(sender, instance,**kwargs):
    firma = instance.firma
    icmaller = Icmal.objects.filter(firma=firma,ay=instance.ay,yıl=instance.yıl)
    atak = 0
    yasalKdv = 0
    tasdik = 0
    kdv = 0
    kdv2 = 0
    muhtasar = 0
    ggkv = 0
    damga = 0
    mtv = 0
    ceza = 0
    idariceza = 0
    davagideri = 0
    hakemheyeti = 0
    geçmişborçlar = 0
    tesvik = 0
    müsavirlik = 0
    harcama = 0
    sgk = 0
    bagkur = 0
    sgkYapilandirmasi =0
    vergiYapilandirmasi=0
    try:
        a = FirmaIcmal.objects.get(firma=firma, ay=instance.ay,yıl=instance.yıl)
    except:
        a = FirmaIcmal(firma=firma,ay=instance.ay,yıl=instance.yıl)
    for icmal in icmaller:
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
        sgkYapilandirmasi += icmal.sgkYapilandirmasi
        vergiYapilandirmasi += icmal.vergiYapilandirmasi
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
    a.vergiYapilandirmasi = vergiYapilandirmasi
    a.sgkYapilandirmasi = sgkYapilandirmasi
    a.save()







