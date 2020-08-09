import os, sys

from django.db import IntegrityError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping.settings'

import django
django.setup()

# Begin parser script
import requests
from bs4 import BeautifulSoup as Bs
from fake_useragent import UserAgent

import json
from scraping_from_ek.models import *


headers = {'User-Agent': UserAgent().chrome}


def get_url(cmp=False):
    all_url = Url.objects.filter(manufacturer__in=['Asus', 'MSI', 'Intel', 'AMD'])

    urls, component = [], []
    for url in all_url:
        component.append(url.component_url)
        urls.append(url.url)

    if cmp:
        return component[0]

    return urls


def get_parse(url):
    resp = requests.get(url, headers=headers)
    html = resp.content

    soup = Bs(html, 'html.parser')
    main_form = soup.find('form', id='list_form1')
    main_div = main_form.find_all('div', class_='model-short-div')
    main_div_v2 = soup.find('div', class_='list-filter')

    result = []
    for item in main_div:
        if not item.find('img'):
            pass
        else:
            img_src = item.find('img')['src']
            title = item.find('a').text
            # find best_cost
            best_cost = item.find('div', class_='sn-div')
            if not best_cost:
                best_cost = 'Информация отсутсвует'
            else:
                best_cost = best_cost.a['onmouseover'][11:-60:]
            # find all price
            price = item.find('div', class_='model-price-range')
            if price:
                price = price.a.text
            else:
                price = item.find('div', class_='pr31').text

            manufacturer_res = ''
            model_res = ''
            for item_v2 in main_div_v2:
                main_a = item_v2.find_all('a', class_='nobr')
                manufacturer = main_a[0].text
                model = main_a[1].text

                manufacturer_res = manufacturer
                model_res = model

            result.append({
                'img': img_src,
                'name': title,
                'wed_price': price,
                'best_price': best_cost,
                'manufacturer': manufacturer_res,
                'model': model_res,
            })
    return result


def run_scraping():
    all_urls = get_url()

    file_name = 'data_scraping.txt'
    my_file = open(file_name, mode='w')

    result_parse = []
    for url in all_urls:
        result_parse += get_parse(url)

    json.dump(result_parse, my_file)
    my_file.close()


def dump_gpu_in_db(key, component):
    if key['best_price'] == 'Информация отсутсвует':
        pass
    else:
        try:
            first_manufacturer = Manufacturer.objects.get(manufacturer_name=key['manufacturer'])
        except:
            Manufacturer.objects.create(manufacturer_name=key['manufacturer'])
            first_manufacturer = Manufacturer.objects.get(manufacturer_name=key['manufacturer'])

        new_gpu = Gpu(img=key['img'], name=key['name'], model=key['model'], wed_price=key['wed_price'],
                      best_price=key['best_price'], manufacturer=first_manufacturer, component=component)
        try:
            new_gpu.save()
        except IntegrityError:
            pass


def dump_cpu_in_db(key, component):
    if key['best_price'] == 'Информация отсутсвует':
        pass
    else:
        try:
            first_manufacturer = Manufacturer.objects.get(manufacturer_name=key['manufacturer'])
        except:
            Manufacturer.objects.create(manufacturer_name=key['manufacturer'])
            first_manufacturer = Manufacturer.objects.get(manufacturer_name=key['manufacturer'])

        new_cpu = Cpu(img=key['img'], name=key['name'], model=key['model'], wed_price=key['wed_price'],
                      best_price=key['best_price'], manufacturer=first_manufacturer, component=component)
        try:
            new_cpu.save()
        except IntegrityError:
            pass


def dump_data_in_db():
    f = open('data_scraping.txt', mode='r')
    data = json.load(f)
    for key in data:
        if key['manufacturer'] != 'Asus' and key['manufacturer'] != 'MSI':
            component = Component.objects.get(component='Процессоры')
        else:
            component = Component.objects.get(component='Видеокарты')

        if component.component == 'Видеокарты':
            dump_gpu_in_db(key, component)
        elif component.component == 'Процессоры':
            dump_cpu_in_db(key, component)


def main():
    # get_url()
    # run_scraping()
    dump_data_in_db()


if __name__ == "__main__":
    main()
