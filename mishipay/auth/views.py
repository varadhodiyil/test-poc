import shopify
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response
from django.contrib.auth import login, logout
from mishipay.auth import serializers
from mishipay.core import models

API_KEY = getattr(settings, 'SHOPIFY_API', '')
API_SECRET = getattr(settings, 'SHOPIFY_SECRET', '')

shop_url = "https://%s:%s@mish-pay.myshopify.com/admin" % (API_KEY, API_SECRET)

shopify.ShopifyResource.set_site(shop_url)
shopify.ShopifyResource.site
# token = shopify_session.request_token(shop_url)

# shop = shopify.Shop(shop=shop_url, token=token)
# Create your views here.


class UserLogin(GenericAPIView):
    """ User Login """
    serializer_class = serializers.UserLoginSerializer
    parser_classes = ((JSONParser, FormParser))
    template_name = 'login.html'

    def get(self, requuest, *args, **kwargs):
        s = self.get_serializer()
        return Response({'fields': s})

    def post(self, request, *args, **kwargs):
        s = serializers.UserLoginSerializer(data=request.data)
        result = dict()
        if s.is_valid():
            email = s.validated_data['email']
            password = s.validated_data['password']
            user = models.Users.objects.filter(email=email)
            if user.count() > 0:
                user = user.get()
                if check_password(password, user.password):
                    login(request, user)
                    result['fields'] = s
                    return redirect('/dashboard/')
                else:
                    result['fields'] = s
                    result['error'] = "Invalid Credentials"
            else:
                result['fields'] = s
                result['error'] = "No user with Email found!"
            return Response(result, status=status.HTTP_200_OK)
        else:

            result['fields'] = s.errors
            return Response(result, status=status.HTTP_200_OK)


class UserRegistration(GenericAPIView):
    """User Registraion"""
    serializer_class = serializers.UserRegistrationSerializer
    parser_classes = ((JSONParser, FormParser))
    template_name = 'register.html'

    def get(self, requuest, *args, **kwargs):
        s = self.get_serializer()
        return Response({'fields': s})

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        if s.is_valid():
            data = dict()
            user = s.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            request.user = user
            return redirect('/dashboard/')
            data['status'] = "Register Successful "
            return Response(data)
        else:
            data = dict()
            data['fields'] = s
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('dashboard')
