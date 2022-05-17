from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('customers', views.customers, name="customers"),
    path('order', views.order, name="order"),
    path('profile', views.profile, name="profile"),
    path('admin', views.admin, name="admin"),
    path('role-change/<token>/', views.roleChange, name='role-change'),
    path('profile/<token>/', views.profile, name='profile'),
    path('edit-profile/<token>/', views.editProfile, name='edit-profile'),
    path('termsandcondition', views.termsandcondition, name="termsandcondition"),
]
