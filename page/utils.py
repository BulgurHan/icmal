from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase

from django.http import HttpResponse
from django.template.loader import get_template

#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.

from xhtml2pdf import pisa  
#difine render_to_pdf() function
from .models import Icmal,Sube,Firma,FirmaIcmal
from django.shortcuts import get_object_or_404



def render_to_pdf(template_src,ay,yil,grup_slug=False,odemeTakip=False,sube_slug=None,firma_slug=None, context_dict={}):
    template = get_template(template_src)
    if  sube_slug  != None and firma_slug !=None:
        firma = Firma.objects.get(slug=firma_slug)
        sube= Sube.objects.get(slug=sube_slug , firma=firma)        
        icmal = Icmal.objects.get(sube = sube, ay=ay, yıl=yil)
        context_dict['icmal'] = icmal
        context_dict['title'] = "Şube İcmali"
    elif firma_slug != None:
        firma= Firma.objects.get(slug=firma_slug)
        icmal = FirmaIcmal.objects.get(firma = firma, ay=ay, yıl=yil )
        context_dict['icmal'] = icmal
        context_dict['title'] = "Firma İcmali"
        context_dict['subeler'] = Sube.objects.filter(firma=firma)
        subeIcmalleri = []
        for sube in context_dict['subeler']:
            try:
                i = Icmal.objects.get(sube=sube, ay=ay, yıl=yil)
                subeIcmalleri.append(i)
            except:
                continue
        context_dict['subeIcmalleri'] = subeIcmalleri  
    elif grup_slug:
        context_dict['title'] = "Ödeme Icmali Görüntüle"
        context_dict['icmaller'] = GrupIcmal.objects.all()
        context_dict['vergilerTop'] = 0
        context_dict['atakTop'] = 0
        context_dict['muhTop'] = 0
        context_dict['defterTop'] = 0
        context_dict['sgkTop'] = 0
        context_dict['bagkurTop'] = 0
        for icmal in context_dict['icmaller']:
            context_dict['vergilerTop']+=icmal.odemelertoplami
            context_dict['atakTop']+=icmal.atak
            context_dict['muhTop']+=icmal.müsavirlikler
            context_dict['defterTop']+=icmal.tasdik
            context_dict['sgkTop']+=icmal.sgk
            context_dict['bagkurTop']+=icmal.bagkur
    elif odemeTakip:
        context_dict['title'] = "Ödeme Takip İcmali Görüntüle"
        context_dict['subeIcmalleri'] = Icmal.objects.filter(ay=ay,yıl=yil)
        context_dict['firmaIcmalleri'] = FirmaIcmal.objects.filter(ay=ay,yıl=yil)
    html  = template.render(context_dict)
    result = BytesIO()

    #This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None