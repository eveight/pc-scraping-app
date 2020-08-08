import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping.settings'

import django
django.setup()

User = get_user_model()
from scraping_from_ek.models import Gpu, Cpu, Errors
from django.core.mail import EmailMultiAlternatives
from dotenv import load_dotenv
load_dotenv()

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


qs_email = User.objects.filter(message=True).values('email')


gpu_component = Gpu.objects.all()[:5]
cpu_component = Cpu.objects.all()[:5]


if gpu_component or cpu_component:
    for email in qs_email:
        html = ''
        html += f'<h2>Мы обновили ценообразование :)</h2>'
        for z in gpu_component:
            html += f'<h4 class="card-title">{ z.name }</h4>'
            html += f'<img src="{ z.img }" class="card-img-top" alt="...">'
            html += f'<p class="card-text">Ценообразование по рынку составляет: { z.wed_price }</p>'
            html += f'<a href="{ z.best_price }" class="btn btn-dark">Лучшая цена на рынке</a>'
        for y in gpu_component:
            html += f'<h4 class="card-title">{y.name}</h4>'
            html += f'<img src="{y.img}" class="card-img-top" alt="...">'
            html += f'<p class="card-text">Ценообразование по рынку составляет: {y.wed_price}</p>'
            html += f'<a href="{y.best_price}" class="btn btn-dark">Лучшая цена на рынке</a>'

        subject, from_email, to = 'Рассылка от PCloves', EMAIL_HOST_USER, email['email']
        text_content = 'Рассылка от PCloves'
        html_content = html
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except ValueError:
            print('Не валдиный имэйл' + email['email'])


errors = Errors.objects.all()
if errors:
    data_d = {}
    for obj in errors:
        data_dir = obj.data['user_data']
        for i in data_dir:
            spisok = data_d.get('data', [])
            spisok.append({'data': i['data'], 'email': i['email']})
            data_d['data'] = spisok

    html = ''
    for items in data_d.values():
        for items_v2 in items:
            html += f'<h2>Ошибки/Предложения</h2>'
            html += f'<p>Предложения: {items_v2["data"]}</p>'
            html += f'<p>От Имэйла: {items_v2["email"]}</p>'

    subject, from_email, to = 'Ошибки от PCloves', EMAIL_HOST_USER, EMAIL_HOST_USER
    text_content = 'Ошибки/Предложения от PCloves'
    html_content = html
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except ValueError:
        print('Не валдиный имэйл')