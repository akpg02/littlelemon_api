from django.contrib.auth.models import User
from rest_framework import serializers
from LittleLemonAPI.models import MenuItem, Category, Cart, OrderItem, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']
        
class DeliveryCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id', 'username', 'email']
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta: 
        model = Order
        fields = ['id', 'delivery_crew', 'status', 'total', 'date', 'items']
        read_only_fields = ['total', 'date', 'items', 'id']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            raise serializers.ValidationError({'cart': 'Your cart is empty.'})
        
        # create the order
        order = Order.objects.create(user=user, total = 0, **validated_data)
        
        total = 0
        order_items = []
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order, 
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            order_items.append(order_item)
            total += cart_item.price
        
            # Bulk create OrderItems and update the order total
        OrderItem.objects.bulk_create(order_items)
        order.items.set(order_items)
        order.total = total
        order.save()
        
        # Clear cart after creating the order
        Cart.objects.filter(user=user).delete()
            
        return order
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
    
        if user.is_superuser or user.groups.filter(name='manager'):
            allowed_fields = ['delivery_crew', 'status']
        elif user.groups.filter(name='delivery_crew').exists():
            allowed_fields = ['status']
        else:
            allowed_fields = []
            
        # Filter the validated data based on allowed fields
        filtered_data = {key: value for key, value in validated_data.items() if key in allowed_fields}
        
        # Update the instance only with allowed fields
        for attr, value in filtered_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
    
    def partial_update(self, instance, validated_data):
        return self.update(instance, validated_data)