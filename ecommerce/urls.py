"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from store import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secure_admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('cart/',views.cart,name='cart'),
    path('products/',views.products,name='products'),
    path('contactus/',views.contactUs,name='contactus'),
    path('aboutus/',views.aboutUs,name='aboutus'),
    path('search/',views.search,name='search'),
    path('checkout/',views.checkout,name='checkout'),
    path('products/<int:myid>/',views.productsView,name='productsview'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('profile/',views.profile,name='profile'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('success/<int:myid>/',views.success,name='success'),
    path('success_handler/',views.success_handler,name='success_handler'),
    path('delete_session/',views.del_session,name='delete_session'),
    path('profile/order-details/<int:myid>/',views.orderDetails,name='orderDetails'),
    path('reviews/<int:myid>/',views.reviews,name='reviews'),
    path('profile/update_address/<int:myid>/',views.update_address,name='update_address'),
    path('profile/change_password/',views.changePassword,name='change_password'),
    path('add_multiple_prod/',views.addmultipleProd,name='add_multiple_prod'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
    path('paytm/',views.paytm,name='paytm'),
    #
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='store/reset_password.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='store/reset_password_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='store/reset_password_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='store/reset_password_complete.html'),name='password_reset_complete'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)