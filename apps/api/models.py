from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        CREATED = "CREATED", "Created"
        PAID = "PAID", "Paid"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        FINISHED = 'FINISHED', 'Finished'
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='CREATED')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_product(self, product, quantity=1):
        if self.status != Order.STATUS_CHOICES.CREATED:
            raise ValueError("Unable to alter the order because it is no longer in 'CREATED' status")

        order_item, created = self.items.get_or_create(product=product)
        if not created:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity
        
        order_item.save()

        self.total_price += product.price * quantity
        self.save()

    def remove_product(self, product, quantity=1):
        if self.status != Order.STATUS_CHOICES.CREATED:
            raise ValueError("Unable to alter the order because it is no longer in 'CREATED' status")
        
        order_item = self.items.filter(product=product).first()
        if not order_item:
            raise ValueError("Product not in order.")

        if order_item.quantity <= quantity:
            self.total_price -= order_item.product.price * order_item.quantity
            order_item.delete()
        else:
            order_item.quantity -= quantity
            self.total_price -= order_item.product.price * quantity
            order_item.save()

        self.save()

    def remove_all_products(self):
        if self.status != Order.STATUS_CHOICES.CREATED:
            raise ValueError("Unable to alter the order because it is no longer in 'CREATED' status")
        
        # Loop through all items in the order and remove them
        for order_item in self.items.all():
            self.total_price -= order_item.product.price * order_item.quantity
            order_item.delete()

        # After removing all products, save the order to update the total price
        self.save()
    
    def change_status(self, new_status):
        self.status = new_status
        self.save()

    def process_payment(self):
        if self.status != Order.STATUS_CHOICES.CREATED:
            raise ValueError("Unable to alter the order because it is no longer in 'CREATED' status")
        if self.total_price == 0:
            raise ValueError("No items in cart")

        # Logic for Payment 
        self.change_status(Order.STATUS_CHOICES.PAID)

    def ship_order(self):
        if self.status != Order.STATUS_CHOICES.PAID:
            raise ValueError("Unable to ship this order, status should be 'PAID'")
        
        self.change_status(Order.STATUS_CHOICES.SHIPPED)

    def finish_order(self):
        if self.status != Order.STATUS_CHOICES.DELIVERED:
            raise ValueError("Unable to ship this order, status should be 'PAID'")

        self.change_status(Order.STATUS_CHOICES.FINISHED)

    def cancel_order(self):
        if self.status in [Order.STATUS_CHOICES.CREATED, Order.STATUS_CHOICES.PAID]:
            self.change_status(Order.STATUS_CHOICES.CANCELLED)
        else:
            raise ValueError("Unable to cancel this order, past point of no return")
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()