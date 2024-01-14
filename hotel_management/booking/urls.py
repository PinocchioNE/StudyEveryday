from django.urls import path
from . import views
from .views import book_room
from .views import staff_register
from .views import staff_login
from .views import login_choice
from .views import staff_home
from .views import check_in
from .views import check_in_success
from .views import staff_manage_bookings
from .views import staff_cancel_booking
from .views import emergency_reports
urlpatterns = [
    # path('rooms/', views.room_list, name='room_list'),
    path('login_choice/', login_choice, name='login_choice'),
    path('register/', views.register, name='register'),
    path('staff_register/', staff_register, name='staff_register'),
    path('staff_login/', staff_login, name='staff_login'),
    path('login/', views.user_login, name='login'),
    path('book_room/', book_room, name='book_room'),
    # path('manage-booking/', views.manage_booking, name='manage_booking'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('booking-list/', views.booking_list, name='booking_list'),
    path('report-emergency/', views.report_emergency, name='report_emergency'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('user_list/', views.user_list, name='user_list'),
    path('staff_home/', staff_home, name='staff_home'),
    path('check_in/', check_in, name='check_in'),
    path('check_in_success/', check_in_success, name='check_in_success'),
    path('staff_manage_bookings/', staff_manage_bookings, name='staff_manage_bookings'),
    path('staff_cancel_booking/<int:booking_id>/', staff_cancel_booking, name='staff_cancel_booking'),
    path('emergency_reports/', emergency_reports, name='emergency_reports'),
]