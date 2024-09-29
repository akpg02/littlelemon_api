from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, viewsets
from config.permissions import MenuItemsPermissions,ManageGroupPermissions, CartPermissions, OrderPermissions
from django.contrib.auth.models import User, Group
from littlelemonAPI.models import MenuItem, Cart, Order
from littlelemonAPI.serializers import MenuItemSerializer, DeliveryCrewSerializer, ManagerSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
# Create your views here.
class MenuItemViewSet(viewsets.ViewSet):
    permission_classes = [MenuItemsPermissions]
    def list(self, request, *args, **kwargs):
        query_set = MenuItem.objects.all()
        serializer = MenuItemSerializer(query_set, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            platform = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Stream platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializer(platform)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk, *args, **kwargs):
        menu_item = MenuItem.objects.get(pk=pk) 
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk, *args, **kwargs):
        platform = MenuItem.objects.get(pk=pk)    
        serializer = MenuItemSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk, *args, **kwargs):
        platform = MenuItem.objects.get(pk=pk)    
        serializer = MenuItemSerializer(platform, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerViewSet(viewsets.ViewSet):
    permission_classes = [ManageGroupPermissions]
    
    def list(self, request, *args, **kwargs):
       try:
           group =  Group.objects.get(name="manager")
           users = group.user_set.all()
           serializer = ManagerSerializer(users, many=True)
           return Response(serializer.data)
       except Group.DoesNotExist:
           return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
       
    def create(self, request, *args, **kwargs):
        try: 
            username = request.data.get('username')
            user = User.objects.get(username = username)
            manager_group = Group.objects.get(name='manager')
            user.groups.add(manager_group)
            return Response({'message': f'{username} added to the Manager group.'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            group = Group.objects.get(name="manager")
            group.user_set.remove(user)
            return Response({'message': f'{user.username} removed from the Manager group.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [ManageGroupPermissions]
    def list(self, request, *args, **kwargs):
       try:
           group =  Group.objects.get(name="delivery_crew")
           users = group.user_set.all()
           serializer = DeliveryCrewSerializer(users, many=True)
           return Response(serializer.data)
       except Group.DoesNotExist:
           return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
       
    def create(self, request, *args, **kwargs):
        try: 
            username = request.data.get('username')
            user = User.objects.get(username=username)
            delivery_group = Group.objects.get(name="delivery_crew")
            user.groups.add(delivery_group)
            return Response({'message': f'{username} added to the Delivery crew group.'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            group = Group.objects.get(name="delivery_crew")
            group.user_set.remove(user)
            return Response({'message': f'{user.username} removed from the Delivery crew group.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
class CartViewSet(viewsets.ViewSet):
    permission_classes = [CartPermissions]
    def list(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.filter(user=request.user)
        except cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
       menuitem = get_object_or_404(MenuItem, pk = request.data['menuitem'])
       data = {}
       data['user'] = self.request.user.id
       data['menuitem'] = menuitem.id
       data['quantity'] = request.data['quantity']
       data['unit_price'] = menuitem.price 
       data['price'] = float(request.data['quantity']) * float(menuitem.price)
       
       serializer = CartSerializer(data=data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user) 
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderViewSet(viewsets.ViewSet):
    permission_classes = [OrderPermissions]
    
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name="manager").exists() or user.is_staff:
            query_set = Order.objects.all()
            serializer = OrderSerializer(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.groups.filter(name="delivery_crew").exists() or user.is_staff:
            query_set = Order.objects.filter(~Q(delivery_crew__isnull=True))
            if query_set.exists():
                serializer = OrderSerializer(query_set, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            # List all orders for the authenticated user
            query_set = Order.objects.filter(user=request.user)
            if not query_set.exists():
                return Response({'error': 'No orders found'}, status=status.HTTP_200_OK)
            serializer = OrderSerializer(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
       
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(id=request.data['delivery_crew'])
        if not user:
            return Response({'error': 'Invalid delivery crew member'}, status=status.HTTP_404_NOT_FOUND)
        
        request.data['delivery_crew'] = user.id
        
        serializer = OrderSerializer(order, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk, *args, **kwargs):
        try: 
            order = Order.objects.get(pk=pk)
            if order.user != request.user:
                return Response({'error': 'You are not authorized to view this order'}, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk, *args, **kwargs):
        # Handle partial updates to an order (PATCH requests)
        try: 
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk, *args, **kwargs):
        try: 
            if request.user.groups.filter(name='manager').exists():
                 order = Order.objects.get(pk=pk)
                 if order: 
                     order.delete()
                     return Response(status=status.HTTP_204_NO_CONTENT)
                 else: 
                     return Response({'error': 'Order not found'}, status=status.HTTP_404_BAD_REQUEST)
            else:
                return Response({'error': 'You do not have permission to delete this order'}, status=status.HTTP_401_UNAUTHORIZED)                 
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)