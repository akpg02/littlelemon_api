from django.db import models
from django.contrib.auth.models import User
from datetime import date 

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    
    def __str__(self) -> str:
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.title}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('menuitem', 'user'),
    
    def __str__(self):
        return str(self.menuitem) + " | " + str(self.quantity) + " | $" + str(self.price)
        
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True, default=None)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f" Order #{self.id} by {self.user.username}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta: 
        unique_together = ('order', 'menuitem')
        
    def __str__(self):
       return f"{self.menuitem.title} (Order: {self.order.id})"

        

    
