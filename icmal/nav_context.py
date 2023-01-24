from page.models import Firma,Sube



def nav_data(request):
    context = dict()
    context['firmalar'] = Firma.objects.all()
    context['subeler'] = Sube.objects.all()
    return context