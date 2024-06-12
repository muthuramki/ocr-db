from django.urls import path
from inte.views import (
    upload_invoice, push_to_sap, login_view, reset_password_view,
    drop_menu_view, register_page_view, UserRegisterView,upload_page_view,home_page_view,forgot_password_view
)

urlpatterns = [
    path('', home_page_view, name='home_page_view'),
    path('upload_invoice', upload_invoice, name='upload_invoice'),
    path('push-to-sap/', push_to_sap, name='push_to_sap'),
    path('login.html', login_view, name='login'),
    path('reset-password.html', reset_password_view, name='reset_password'),
    path('drop-menu.html', drop_menu_view, name='drop_menu'),
    path('register.html', register_page_view, name='register_view'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('upload.html', upload_page_view, name='upload_view'),
    path('forgot-password.html', forgot_password_view, name='forgot_password_view'),
    path('drop-menu/', drop_menu_view, name='drop-menu'),

]
