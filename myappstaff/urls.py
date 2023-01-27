from django.urls import path
from myappstaff import views
from .views import * 

urlpatterns = [
    # staff
    
    path('staff_index_borrow', views.staff_index_borrow, name="staff_index_borrow"),
    path('staff_index_borrow_durable', views.staff_index_borrow_durable, name="staff_index_borrow_durable"),
    path('staff_index_borrownow', views.staff_index_borrownow, name="staff_index_borrownow"),
        
        
    path('staff_borrowing_history', views.staff_borrowing_history, name="staff_borrowing_history"),
    path('staff_borrowing_history_durable', views.staff_borrowing_history_durable, name="staff_borrowing_history_durable"),

    path('staff_return_durable/<int:id>', views.staff_return_durable, name="staff_return_durable"),
    path('staff_unreturn_durable/<int:id>', views.staff_unreturn_durable, name="staff_unreturn_durable"),
    path('staff_index_return', views.staff_index_return, name="staff_index_return"),
    
    path('staff_borrow_parcel/<int:id>', views.staff_borrow_parcel, name="staff_borrow_parcel"),
    path('staff_unborrow_parcel/<int:id>', views.staff_unborrow_parcel, name="staff_unborrow_parcel"),
    path('staff_borrow_durable/<int:id>', views.staff_borrow_durable, name="staff_borrow_durable"),
    path('staff_unborrow_durable/<int:id>', views.staff_unborrow_durable, name="staff_unborrow_durable"),
    
    path('staff_introduction_detail/<int:id>', views.staff_introduction_detail, name="staff_introduction_detail"),
    path('staff_introduction', views.staff_introduction, name="staff_introduction"),
    path('staff_introduction_update/<int:id>', views.staff_introduction_update, name="staff_introduction_update"),
    path('staff_introduction_history', views.staff_introduction_history, name="staff_introduction_history"),
   
    path('staff_personal_info', views.staff_personal_info, name="staff_personal_info"),
    path('staff_admin_user', views.staff_admin_user, name="staff_admin_user"),
    path('staff_admin_user_block', views.staff_admin_user_block, name="staff_admin_user_block"),
    path('staff_user_deadline/<int:id>', views.staff_user_deadline, name="staff_user_deadline"),

    path('staff_max_borrow', views.staff_max_borrow, name='staff_max_borrow'),
    path('staff_max_borrow_durable', views.staff_max_borrow_durable, name='staff_max_borrow_durable'),
    
    path('staff_report/', views.staff_report, name="staff_report"),
    
    path('staff_queue/', views.staff_queue, name="staff_queue"),
    path('staff_queue_durable/', views.staff_queue_durable, name="staff_queue_durable"),
    
    #path manage parcel durable
    path('staff_manage_detail/<int:id>', views.staff_manage_detail, name="staff_manage_detail"),
    path('staff_manage_detail_durable/<int:id>', views.staff_manage_detail_durable, name="staff_manage_detail_durable"),
    #path('edit_staff_manage_detail/<int:id>', views.edit_staff_manage_detail, name="edit_staff_manage_detail"),
    path('delete_staff_manage_detail/<int:id>', views.delete_staff_manage_detail, name="delete_staff_manage_detail"),
    
    path('staff_manage_parcel', views.staff_manage_parcel, name="staff_manage_parcel"), #add parcel
    path('delete_staff_manage_parcel/<int:id>',views.delete_staff_manage_parcel, name="delete_staff_manage_parcel"), #delete
    path('edit_staff_manage_parcel/<int:id>',views.edit_staff_manage_parcel, name="edit_staff_manage_parcel"), #edit
    
    path('staff_manage_durable', views.staff_manage_durable, name="staff_manage_durable"),#add durable
    path('delete_staff_manage_durable/<int:id>',views.delete_staff_manage_durable, name="delete_staff_manage_durable"),
    path('edit_staff_manage_durable/<int:id>',views.edit_staff_manage_durable, name="edit_staff_manage_durable"), #edit
    
    path('pdf_print',views.pdf_print, name='pdf_print'),
    path('pdf_borrow',views.pdf_borrow, name='pdf_borrow'),
    path('pdf_borrow_durable',views.pdf_borrow_durable, name='pdf_borrow_durable'),
    path('pdf_print_position',views.pdf_print_position, name='pdf_print_position'),
    path('pdf_staff_max_borrow',views.pdf_staff_max_borrow, name='pdf_staff_max_borrow'),
    path('pdf_staff_max_borrow_durable',views.pdf_staff_max_borrow_durable, name='pdf_staff_max_borrow_durable'),
    path('pdf_staff_parcel',views.pdf_staff_parcel, name='pdf_staff_parcel'),
    path('pdf_staff_durable',views.pdf_staff_durable, name='pdf_staff_durable'),
    path('pdf_staff_queue',views.pdf_staff_queue, name='pdf_staff_queue'),
    path('pdf_staff_queue_durable',views.pdf_staff_queue_durable, name='pdf_staff_queue_durable'),
    
    #path staff_setting
    path('staff_setting',views.staff_setting, name="staff_setting"), 
    path('deleteCategoryType/<int:id>',views.deleteCategoryType, name="deleteCategoryType"),
    path('edit_staff_setting/<int:id>',views.edit_staff_setting, name="edit_staff_setting"),
    
    path('staff_setting_status',views.staff_setting_status, name='staff_setting_status'),
    path('DeleteCategoryStatus/<int:id>',views.DeleteCategoryStatus, name="DeleteCategoryStatus"),
    path('edit_staff_setting_status/<int:id>',views.edit_staff_setting_status, name="edit_staff_setting_status"),
    
    path('staff_position',views.staff_position, name='staff_position'),
    path('staff_setting_position',views.staff_setting_position, name='staff_setting_position'),
    path('deletePosition/<int:id>',views.deletePosition, name="deletePosition"),
    path('edit_position/<int:id>',views.edit_position, name="edit_position"),
    
]
