from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.conf.urls import url


urlpatterns=[
    path('',views.indexView,name="home"),
    path('dashboard/', views.dashboardView,name="dashboard_url"),
    path('login/', views.loginView, name="login_url"),
    path('register/', views.registerView, name="register_url"),
    path('logout/', views.logoutView,name="logout_url"),
    path('profile/', views.profileView, name="profile_url"),
    path('admin/', views.adminView, name="admin"),
    path('bookpage/', views.bookpageView, name="bookpage_url"),
    path('historypage/', views.historypageView, name="historypage_url"),
    path('romancepage/', views.romancepageView, name="romancepage_url"),
    path('fantasypage/', views.fantasypageView, name="fantasypage_url"),
    path('mysterypage/', views.mysterypageView, name="mysterypage_url"),
    path('firstbook/', views.firstbookView, name="firstbook_url"),
    path('checkout/', views.checkoutView, name="checkout_url"),
    path('ordercomplete/', views.ordercompleteView, name="ordercomplete_url"),
    path('orderhistory/', views.orderhistoryView, name = "orderhistory_url"),
    path(r'^add_to_cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    path(r'^go_to_page/(?P<item_id>[-\w]+)/$', views.go_to_page, name="go_to_page"),
    path(r'^remove_from_cart/(?P<item_id>[-\w]+)/$', views.remove_from_cart, name="remove_from_cart")

]