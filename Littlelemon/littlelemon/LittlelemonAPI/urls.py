from django.urls import path
from . import views


urlpatterns = [
    path('menu-items', views.MenuItemsListView.as_view()),
    path('menu-items/<int:pk>', views.SingleItemVIew.as_view()),
    path('cart-view',views.CartView.as_view()),
    path('group/manager/users',views.ManagerView.as_view()),
    path('group/manager/users/<int:pk>/', views.ManagerDeleteView.as_view()),
    path('group/delivery-crew/users', views.DeleiveryCrewListView.as_view()),
    path('group/delivery-crew/users/<int:pk>', views.DeliveryCrewDeleteView.as_view()),
]