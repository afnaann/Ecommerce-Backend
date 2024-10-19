import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db import transaction
import stripe

from cart.models import Cart, CartItem
from orders.models import Order, OrderItems

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):
    def post(self,request):
        data = request.data
        cart = data.get('cart')
        
        line_items = []
        total_amount = 0
                
        for each in cart:
            line_items.append({
                'price_data': {
                    'currency':'inr',
                    'product_data':{
                        'name': each['product']['name']
                    },
                    'unit_amount':int(each['product']['price'] * 100),
                },
                'quantity':each['quantity'],
            })
            total_amount += each['product']['price'] * each['quantity']
        
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                shipping_address_collection={
                    'allowed_countries': ['IN','LK']
                },
                mode='payment',
                success_url=f'http://localhost:5173/ordersuccess/?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url='http://localhost:5173/shop',
            )
            return Response({'id': session.url}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            
class ProcessOrderView(APIView):
    def get(self, request):
        session_id = request.GET.get('session_id')
        print('session',session_id)
        if not session_id:
            return Response({'error':'Missing Session Id'},status=status.HTTP_404_NOT_FOUND)
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            print(session)
            shipping_address = session.shipping_details.address
            print(shipping_address)
            print(request.user.id)
            
            user = request.user
            
            cart = Cart.objects.get(user=user)
            
            cartItems = CartItem.objects.filter(cart=cart)
            
            
            print(cart)
            with transaction.atomic():  
                order = Order.objects.create(
                    user = request.user,
                    address=f"{shipping_address['line1']}, {shipping_address['city']}, {shipping_address['postal_code']}, {shipping_address['country']}",
                    total_price = session.amount_total / 100
                )
                print(order)
                
                for item in cartItems:
                    product_id = item.product.id
                    quantity = item.quantity
                    OrderItems.objects.create(order=order,product_id=product_id,quantity=quantity)

            return Response({'status':'Order Created Successfully!'},status=status.HTTP_201_CREATED)
        except Exception as e:
            print('errrrr',e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
