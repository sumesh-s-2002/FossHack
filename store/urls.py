from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
#urls patterns
urlpatterns = [
    path("", views.home, name="Home-page"),
    path("contacts/", views.contacts, name="Contacts-page"),
    path("products/", views.products, name="Products-page"),
    path("cart/", views.cart, name="Cart-page"),
    path("login/", views.login, name="Login-page"),
    path("register/", views.register, name="Register-page"),
    path("myprofile/", views.myprofile, name="Myprofile-page"),
    path("cart/checkout/", views.checkout, name="Checkout-page"),
    path("logout/", views.logout, name="LogOut-page"),
    path("addtocart/", views.addToCart, name="addtocart-page"),
    path("updatecart/", views.updateCart, name="updatecart-page"),
    path("password-reset/", auth_view.PasswordResetView.as_view(template_name='store/password-reset.html'), name='password_reset'),
    path("password-reset/done/", auth_view.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'), name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>", auth_view.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'), name='password_reset_confirm'),
    path("password-reset-complete", auth_view.PasswordResetCompleteView.as_view(template_name='store/password-reset-complete.html'), name='password_reset_complete'),
    path("product-details/<str:id>/" ,views.productDetails, name="Product-details"),
    path("payment/" ,views.payment, name="payment-page"),
    path("payment/paymenthandler/" ,views.paymentHandler, name="payment-handler"),


 
]