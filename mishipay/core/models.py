from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
	objects = models.Manager()
	address = models.TextField(null=True,default=None)
	class Meta:
		unique_together = ('email',)
		db_table = "users"

class Cart(models.Model):
	objects = models.Manager()
	
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users,on_delete=models.CASCADE)
	product = models.CharField(max_length=20)
	varient = models.CharField(max_length=20)
	added_at = models.DateTimeField(auto_now=True)
	price = models.FloatField()
	is_paid = models.BooleanField(default=False)
	class Meta:
		db_table = "cart"


class Orders(models.Model):
	objects = models.Manager()
	id = models.AutoField(primary_key=True)
	total_amount = models.FloatField()
	ordered_at = models.DateTimeField(auto_now=True)
	order_id = models.CharField(max_length=20)
	user = models.ForeignKey(Users,on_delete=models.CASCADE)
	class Meta:
		db_table = "orders"

class PaymentCards(models.Model):
	last4 = models.IntegerField()
	expiry = models.CharField(max_length=5)
	user = models.ForeignKey(Users,on_delete=models.CASCADE)

	class Meta:
		db_table = "payment_cards"