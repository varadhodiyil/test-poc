from rest_framework import serializers
from mishipay.core import models
from django.utils.timesince import timesince
import shopify
class AddToCartSerializer(serializers.Serializer):
	product = serializers.CharField()
	varient = serializers.CharField()
	class Meta:
		fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		data = super(CartSerializer, self).to_representation(instance)
		product = shopify.Product.find(instance.product).to_dict()
		varient = []
		for v in product['variants']:
			if v['id'] == int(instance.varient):
				varient = v
		product['variants'] = varient
		data.update(product)
		data['added_at'] = timesince(instance.added_at)
		data['cart_id'] = instance.id
		return data
	class Meta:
		fields = '__all__'
		model = models.Cart

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Users
		fields = ['first_name','last_name','address']


class OrderSerialzer(serializers.ModelSerializer):
	def to_representation(self, instance):
		data = super(OrderSerialzer, self).to_representation(instance)
		# data['cart'] = [CartSerializer(instance.cart).data]
		data['ordered_at'] = timesince(instance.ordered_at)
		data.update( shopify.Order.find(instance.order_id).to_dict())
		return data
	class Meta:
		model = models.Orders
		fields = '__all__'


class OrderCartSerializer(serializers.Serializer):
	cart = serializers.IntegerField(required=False)
	class Meta:
		fields = '__all__'

class PaymentCardSerializer(serializers.ModelSerializer):
	card_number = serializers.CharField(max_length=16)
	cvc = serializers.CharField(max_length=3)

	class Meta:
		models = models.PaymentCards
		fields = '__all__'