from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home and product pages
    path('', views.home, name='home'),
    path('product-detail/', views.product_detail, name='product-detail'),
    path('buy/', views.buy_now, name='buy-now'),

    # User authentication and profile
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.Cus_register, name='Cus_register'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('profile/', views.profile_page, name='profile_page'), 

    # Order and cart-related URLs
    path('place-order/', views.place_order, name='place_order'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('update_cart/', views.update_cart, name='update_cart'),

    # Checkout and order summary
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_summary, name='orders'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),


    # Miscellaneous
    path('address/', views.address, name='address'),
    path('mobile/', views.mobile, name='mobile'),
    path('test-auth/', views.test_auth, name='test-auth'),
    path('index/', views.index, name='index'),
    path('fetch', views.fetch, name='fetch'),
    path('final/', views.final, name='final'),

]

# Serve media and static files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
