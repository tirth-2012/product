from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('user_login',views.user_login,name='userlogin'),
    path('user_login/',views.user_login,name='userlogin'),
    path('user_logout',views.user_logout,name='userlogout'),
    path('search',views.search,name='saerch'),
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('subcategory/<slug:slug>/', views.subcategory_products, name='subcategory_products'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('showproduct',views.showproduct,name='showproduct'),
    path('editproduct/<int:pk>',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:pk>',views.deleteproduct,name='deleteproduct'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('showcategory',views.showcategory,name='showcategory'),
    path('editcategory/<int:pk>',views.editcategory,name='editcategory'),
    path('deletecategory/<int:pk>',views.deletecategory,name='deletecategory'),
    path('addsubcategory',views.addsubcategory,name='addsubcategory'),
    path('viewproduct/<int:pk>',views.viewproduct,name='viewproduct'),
    path('addtocart/<int:pk>',views.addtocart,name='addtocart'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('category/<int:category_id>/', views.productcategory, name='productcategory'),
    path('chechout',views.chechout,name='checkout'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
