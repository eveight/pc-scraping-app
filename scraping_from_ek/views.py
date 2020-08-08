from django.shortcuts import render

from scraping_from_ek.models import *


def home(request):
    qs1 = Gpu.objects.all()
    qs2 = Cpu.objects.all()
    qs = qs1.union(qs2)

    ctx = {
        'qs': qs,
        'all_cmpnt': get_all_component(),
    }
    return render(request, 'scraping_from_ek/home.html', ctx)


def home_list(request):
    # get all model for filter
    all_model = Gpu.objects.all()
    models = []
    for i in all_model:
        if i.model not in models:
            models.append(i.model)

    cmp = request.GET['component']

    ctx = {
        'all_cmpnt': get_all_component(),
        'all_manufacturer': get_all_manufacturer(),
        'models': models,
    }
    # filter by component
    if cmp:
        component_show = Gpu.objects.filter(component__component=cmp)
        if component_show:
            ctx['qs'] = component_show
        component_show = Cpu.objects.filter(component__component=cmp)
        if component_show:
            ctx['qs'] = component_show

    return render(request, 'scraping_from_ek/home_list.html', ctx)


def home_list_filter(request):
    model = request.GET.getlist('model')
    manufacturer = request.GET.getlist('manufacturer')

    ctx = {
        'all_cmpnt': get_all_component(),
    }

    _filter = {}
    if manufacturer:
        _filter['manufacturer__manufacturer_name__in'] = manufacturer
    if model:
        _filter['model__in'] = model

    component_show = Gpu.objects.filter(**_filter)
    component_show2 = Cpu.objects.filter(**_filter)
    qs = component_show.union(component_show2)

    ctx['qs'] = qs

    return render(request, 'scraping_from_ek/home_list.html', ctx)


def get_all_component():
    all_cmpnt = Component.objects.all()
    return all_cmpnt


def get_all_manufacturer():
    all_manufacturer = Manufacturer.objects.all()
    return all_manufacturer
