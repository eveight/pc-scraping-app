import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, RegistrationForm, UpdateUserForm, Contact
from django.contrib import messages

from scraping_from_ek.models import Errors

User = get_user_model()


def login_view(request):
    form_login = LoginForm()
    if request.method == 'POST':
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('login')

    return render(request, 'accounts/login.html', {'form_login': form_login})


def registration_view(request):
    register_form = RegistrationForm()
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Новый пользователь успешно создан.')
            return render(request, 'accounts/registration_done.html', {'new_user': new_user})
    return render(request, 'accounts/registration.html', {'register_form': register_form})


def update_user_view(request):
    contact_form = Contact()
    if request.user.is_authenticated:
        user = request.user
        form = UpdateUserForm(initial={
            'message': user.message,
        })
        if request.method == 'POST':
            form = UpdateUserForm(request.POST)
            if form.is_valid():
                user.message = form.cleaned_data['message']
                user.save()
                messages.success(request, 'Ваш профиль успешно обновлён.')
                return redirect('update_user_view')
        return render(request, 'accounts/update_user.html', {
                                                            'form': form,
                                                            'contact_form': contact_form,
                                                            })
    else:
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('/')


def delete_view(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user.delete()
        messages.error(request, 'Ваш профиль был удалён.')
        return redirect('home')
    else:
        return redirect('login')


def contact(request):
    if request.method == "POST":
        form = Contact(request.POST)
        if form.is_valid():
            data = form.cleaned_data['comp']
            email = form.cleaned_data['email']
            qs = Errors.objects.filter(time=datetime.date.today())
            if qs.exists():
                upd = qs.first()
                data_user = upd.data.get('user_data', [])
                data_user.append({'data': data, 'email': email})
                upd.data['user_data'] = data_user
                upd.save()
            else:
                data = {'user_data': [{'data': data, 'email': email}]}
                Errors.objects.create(data=data)
        messages.success(request, 'Ваша просьба отправлена администрации сайта.')
        return redirect('update_user_view')

    else:
        return redirect('update_user_view')