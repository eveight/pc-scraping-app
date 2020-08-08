from django.urls import path

from accounts import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registration', views.registration_view, name='registration'),
    path('update-user', views.update_user_view, name='update_user_view'),
    path('delete-user', views.delete_view, name='delete_view'),
    path('contact', views.contact, name='contact'),
]
