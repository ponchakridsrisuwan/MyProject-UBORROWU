from django.urls import path
from .views import * 
from myapp import views

urlpatterns = [
    path('',views.HomePage, name="user_index"),
    path('phone_add_number',views.phone_add_number, name="phone_add_number"), 
    
    path('user_borrow',views.user_borrow, name="user_borrow"), 
    path('user_borrow_durable',views.user_borrow_durable, name="user_borrow_durable"), 
    path('confirm_parcel/<int:id>',views.confirm_parcel, name="confirm_parcel"), 
    path('confirm_durable/<int:id>',views.confirm_durable, name="confirm_durable"), 
    path('return_durable/<int:id>',views.return_durable, name="return_durable"), 
    
    path('user_borrowed',views.user_borrowed, name="user_borrowed"), 
    path('user_history',views.user_history, name="user_history"), 
    path('user_history_durable',views.user_history_durable, name="user_history_durable"), 
    
    path('user_cart',views.user_cart, name="user_cart"), 
    path('add_to_cart/<int:id>',views.add_to_cart, name="add_to_cart"), 
    path('cart_update/<int:id>', views.cart_update, name="cart_update"),
    path('cart_notupdate/<int:id>', views.cart_notupdate, name="cart_notupdate"),
    path('cart_update_durable/<int:id>', views.cart_update_durable, name="cart_update_durable"),
    path('cart_notupdate_durable/<int:id>', views.cart_notupdate_durable, name="cart_notupdate_durable"),
    
    path('delete_add_to_cart/<int:id>',views.delete_add_to_cart, name="delete_add_to_cart"), 
    path('add_multiple_to_borrow_parcel',views.add_multiple_to_borrow_parcel, name="add_multiple_to_borrow_parcel"), 
    path('delete_borrow_parcel/<int:id>',views.delete_borrow_parcel, name="delete_borrow_parcel"), 
    
    path('user_queue',views.user_queue, name="user_queue"), 
    path('user_queue_durable',views.user_queue_durable, name="user_queue_durable"), 
    path('delete_queue/<int:id>',views.delete_queue, name="delete_queue"), 
    path('delete_queue_durable/<int:id>',views.delete_queue_durable, name="delete_queue_durable"), 
    
    path('add_to_cart_durable/<int:id>',views.add_to_cart_durable, name="add_to_cart_durable"), 
    path('delete_durable_add_to_cart/<int:id>',views.delete_durable_add_to_cart, name="delete_durable_add_to_cart"), 
    
    path('add_multiple_to_borrow_durable',views.add_multiple_to_borrow_durable, name="add_multiple_to_borrow_durable"), 
    path('delete_borrow_durable/<int:id>',views.delete_borrow_durable, name="delete_borrow_durable"), 
    
    path('user_detail/<int:id>',views.user_detail, name="user_detail"), 
    path('user_detail_durable/<int:id>',views.user_detail_durable, name="user_detail_durable"),  
    path('user_durable_articles',views.user_durable_articles, name="user_durable_articles"), 
    
    path('user_recommend',views.user_recommend, name="user_recommend"), 
    path('user_recommend_edit/<int:id>',views.user_recommend_edit, name="user_recommend_edit"),
    path('deleteRecList/<int:id>', views.deleteRecList, name="deleteRecList"),
    path('user_recommend_history/',views.user_recommend_history, name="user_recommend_history"), 
    path('user_recommend_detail/<int:id>', views.user_recommend_detail, name="user_recommend_detail"),
    
    path('user_personal_info', views.user_personal_info, name="user_personal_info"),
    path('user_position', views.user_position, name="user_position"),
    
    path('pdf_print_position', views.pdf_print_position, name="pdf_print_position"),
    
    
]