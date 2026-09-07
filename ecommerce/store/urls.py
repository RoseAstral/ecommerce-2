from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  (
    buyer_register_view,
    frontpage,
    vender_register_view,
    login_view,
    add_store_view,
    update_store_view,
    delete_store_view,
    logout_view,
    add_product_view,
    update_product_view,
    delete_product_view,
    store_details_view,
    product_details_view,
    add_review_view,
    add_item_to_cart_view,
    view_cart_view,
    send_invoice,
    add_product_api_view,
    view_product_api_view,
    add_store_api_view,
    view_store_api_view,
    view_review_api_view
)

urlpatterns = [
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
     
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
     
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
     
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),

    path('review_get_api/', view_review_api_view, name='view_review_api'),

    path('add_store_api/', add_store_api_view, name='add_store_api'),

    path('add_product_api/', add_product_api_view, name='add_product_api'),

    path('product_details_api/', view_product_api_view, name='view_product_api'),

    path('store_details_api/', view_store_api_view, name='view_store_api'),

    path('send_invoice/', send_invoice, name="send_invoice"),

    path('cart/', view_cart_view, name="view_cart"),

    path('add_to_cart/<int:pk>/', add_item_to_cart_view, name='add_to_cart'),
    
    path('product_details/<int:pk>/add_review/', add_review_view, name='add_review'),

    path('product_details/<int:pk>/', product_details_view, name='product_details'),
    
    path('store_details/<int:pk>/', store_details_view, name="store_details"),

    path('delete_product/<int:pk>/', delete_product_view, name='delete_product'),

    path('edit_product/<int:pk>/', update_product_view, name="edit_product"),

    path('store_details/<int:pk>/add_product/', add_product_view, name='add_product'),

    path('logout/', logout_view, name='logout'),

    path('delete_store/<int:pk>/', delete_store_view, name='delete_store'),

    path('edit_store/<int:pk>/', update_store_view, name="edit_store"),

    path("add_store/", add_store_view, name="add_store"),

    path("accounts/login/", login_view, name="login"),

    path("registervender/", vender_register_view, name="vender_register"),

    path("", frontpage, name="frontpage"),
    
    path("registerbuyer/", buyer_register_view, name="buyer_register")

]
