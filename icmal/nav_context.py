from page.models import Firma



def nav_data(request):
    context = dict()
    context['firmalar'] = Firma.objects.all()
    return context