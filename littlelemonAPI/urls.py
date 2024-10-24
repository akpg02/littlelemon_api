from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_app.views import registration_view, user_view
from LittleLemonAPI.views import MenuItemViewSet, ManagerViewSet, DeliveryCrewViewSet, CartViewSet, OrderViewSet, CategoryViewSet

router = DefaultRouter()
router.register('menu-items', MenuItemViewSet, basename='menu-items')
router.register('cart/menu-items', CartViewSet, basename='cart-menu-items')
router.register('groups/manager/users', ManagerViewSet, basename='manager-users')
router.register('groups/delivery-crew/users', DeliveryCrewViewSet, basename='delivery-crew-users')
router.register('orders', OrderViewSet, basename='orders')
router.register('orders/<int:pk>/', OrderViewSet, basename='order-item')
router.register('categories', CategoryViewSet, basename='categories')
router.register('categories/<int:pk>', CartViewSet, basename='category-item')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', registration_view, name='register'),
    path('users/users/me/', user_view, name='user_info'),
]