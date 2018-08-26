import json

import shopify
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response

from mishipay.core import models, serializers

# Create your views here.

API_KEY = getattr(settings, 'SHOPIFY_API', '')
API_SECRET = getattr(settings, 'SHOPIFY_SECRET', '')

shop_url = "https://%s:%s@mish-pay.myshopify.com/admin" % (API_KEY, API_SECRET)

shopify.ShopifyResource.set_site(shop_url)
shopify.ShopifyResource.site

location = shopify.Location.find(page=1)


class Dashboard(GenericAPIView):

    def get(self, request, *args, **kwargs):
        data = shopify.Product.find(limit=50, page=1)
        data = [c.to_dict() for c in data]
        response = dict()
        # with open("E:\D\Xtreme Me\WebApps\mishipay\mishipay\mishipay\core\data.json", "r") as h:
        # 	data = json.load(h)
        response['products'] = data
        return Response(response, template_name='dashboard.html')


class Cart(GenericAPIView):
    parser_classes = ((JSONParser, FormParser))
    serializer_class = serializers.AddToCartSerializer

    def get(self, request, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            carts = models.Cart.objects.filter(
                user=request.user, is_paid=False).order_by("-added_at")
            result['products'] = serializers.CartSerializer(
                carts, many=True).data
            return Response(result, template_name='cart.html')
        else:
            result['status'] = False
            result['error'] = "Unauthorized"
            return Response(result)

    def post(self, request, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            s = self.get_serializer(data=request.data, many=True)
            if s.is_valid():
                for d in s.validated_data:
                    product = shopify.Product.find(d['product'])
                    varient = d['varient']
                    has_element = False
                    for v in product.variants:
                        if v.id == int(varient):
                            models.Cart(user=request.user, product=product.id,
                                        varient=varient, price=v.price).save()
                            has_element = True
                    result['has_varient'] = has_element
                result['status'] = True
                return Response(result)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result)
        else:
            result['status'] = False
            result['error'] = "Unauthorized"
            return Response(result)


class UpdateCart(GenericAPIView):
    parser_classes = ((JSONParser, FormParser))

    def delete(self, request, cart, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            models.Cart.objects.filter(user=request.user, id=cart).delete()
            has_element = True
            result['has_varient'] = has_element
            result['status'] = True
            return Response(result)
        else:
            result['status'] = False
            result['error'] = "Unauthorized"
            return Response(result)


class Profile(UpdateAPIView):
    parser_classes = ((JSONParser, FormParser))
    serializer_class = serializers.ProfileSerializer
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        result = dict()
        if request.is_ajax():
            s = self.get_serializer(request.user)
            result = s.data
            return Response({})
        else:
            if request.user.is_authenticated:
                s = self.get_serializer(request.user)
                if not request.is_ajax():
                    result['fields'] = s
                return Response(result)
            else:
                result['status'] = False
                return redirect('/login/')

    def post(self, request, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            s = self.get_serializer(data=request.data, instance=request.user)
            if s.is_valid():
                s.save()
                result['status'] = True
                if not request.is_ajax():
                    result['fields'] = s
                return Response(result)
            else:
                result['status'] = False
                if not request.is_ajax():
                    result['fields'] = s
                result['errors'] = s.errors
                return Response(result)
        else:
            result['status'] = False
            result['error'] = "Unauthorized"
            return Response(result)


class Orders(GenericAPIView):
    serializer_class = serializers.OrderSerialzer
    parser_classes = ((JSONParser, FormParser))

    def get(self, request, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            orders = models.Orders.objects.filter(
                user=request.user).order_by("-ordered_at")
            s = self.get_serializer(orders, many=True)
            # if request.is_ajax():
            result['orders'] = s.data
            result['status'] = True
            return Response(result, template_name='orders.html')

        else:
            result['status'] = False
            result['error'] = "Unauthorized"
            return Response(result)

    def post(self, request, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            s = serializers.OrderCartSerializer(data=request.data)
            if s.is_valid():
                order = shopify.Order()
                order.email = request.user.email
                order.fulfillment_status = "fulfilled"
                order.send_receipt = True
                order.send_fulfillment_receipt = False
                order.line_items = []
                carts = models.Cart.objects.filter(
                    user=request.user, is_paid=False)
                total_price = 0
                for cart in carts:
                    cart.is_paid = True
                    product = shopify.Product.find(cart.product)
                    for v in product.variants:
                        if v.id == int(cart.varient):
                            order.line_items.append(
                                {"variant_id": v.id, "quantity": 1})
                            shopify.InventoryLevel.set(
                                location[0].id, v.inventory_item_id, v.inventory_quantity - 1)
                            success = True
                            total_price = total_price + float(v.price)

                            cart.save()
                success = order.save()
                models.Orders(total_amount=total_price,
                              order_id=order.id, user=request.user).save()
                result['status'] = success
                return Response(result, template_name='orders.html')
            else:

                result['status'] = False
                result['error'] = "Bad Request"
                return Response(result)
        else:
            result['status'] = False
            result['error'] = "Unauthorized"
            return Response(result)


class PaymentCards(GenericAPIView):
    parser_classes = ((JSONParser, FormParser))
    serializer_class = serializers.PaymentCardSerializer

    def get(self, request, *args, **kwargs):
        pass
