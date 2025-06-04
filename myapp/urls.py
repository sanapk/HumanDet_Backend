from django.urls import path, include
from myapp import views

urlpatterns = [
    path('adminhome/',views.adminhome),
    path('login/',views.login),
    path('loginpost/',views.loginpost),
    path('Change_password/',views.Change_password),
    path('change_password_post/',views.change_password_post),
    path('view_user/',views.view_user),
    path('view_user_post/',views.view_user_post),
    path('view_c_r/',views.view_c_r),
    path('view_c_r_post/',views.view_c_r_post),
    path('reply_complaint/<id>',views.reply_complaint),
    path('reply_complaint_post/',views.reply_complaint_post),
    path('logout/',views.logout),

    path('flutt_signup_post/', views.flutt_signup_post),
    path('userlogin/', views.userlogin),
    path('view_user_profile/', views.view_user_profile),
    path('edit_user_profile/', views.edit_user_profile),
    path('user_viewreply/', views.user_viewreply),
    path('user_sendcomplaint/', views.user_sendcomplaint),
    path('user_changepassword/', views.user_changepassword),
    path('user_check/', views.user_check),

]