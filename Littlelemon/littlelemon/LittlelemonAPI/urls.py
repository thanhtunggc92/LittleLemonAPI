from django.urls import path
from . import views


urlpatterns = [
    path('menu-items', views.MenuItemsListView.as_view()),
    path('menu-items/<int:pk>', views.SingleItemVIew.as_view()),
    path('cart-view',views.CartView.as_view()),
    path('manager/group/users',views.ManagerView.as_view())
    
]