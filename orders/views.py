from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from cart.models import CartItemModel

from orders.models import OrderModel, OrderProductModel, PaymentModel
from store.models import Product
from .forms import OrderForm

import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = OrderModel.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    # print(body)

# store transaction details inside payment model
    payment = PaymentModel(
        user = request.user,
        payment_id = body['transactionID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    ) 
    payment.save()
# after this order is successful
    order.payment = payment
    order.is_ordered = True
    order.save()


# move the cart items to Order Product table 

    # get all the cart items acc to user
    cart_items = CartItemModel.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProductModel()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product.id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.discounted_price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItemModel.objects.get(id=item.id) # getting all items in the cart by id
        product_variation = cart_item.variations.all() # getting all the variations in the cart items
        orderproduct = OrderProductModel.objects.get(id=orderproduct.id) # getting the product ordered
        orderproduct.variation.set(product_variation) # and setting its variations to the variations in the cart 
        orderproduct.save()

# reduce the quantity of sold products
        product = Product.objects.get(id=item.product.id)
        product.stock -= item.quantity
        product.save()

# clear cart 
    CartItemModel.objects.filter(user=request.user).delete()

# send order received email to customer
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order':order,
       
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

# send order number and transaction id back to sendData method via json response
    data = {
        'order_number': order.order_number,
        'transactionID':payment.payment_id,
    }

    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    current_user = request.user

# if cart count <= 0 then redirect back to shop
    cart_items = CartItemModel.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.discounted_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total ) /100
    grand_total = total + tax
        
# case 2 - if user fills all the details
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
        # store all the billing info inside order table
            data = OrderModel()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = grand_total
            data.tax = tax

            data.ip = request.META.get('REMOTE_ADDR') # gives user ip
            data.save()

        # generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d") #20220129(today's date)
            order_number = current_date + str(data.id)

            data.order_number = order_number
            data.save()

            order = OrderModel.objects.get(user=current_user, is_ordered=False,order_number=order_number )
            context = {'order':order, 'cart_items': cart_items, 'total':total, 'tax':tax, 'grand_total': grand_total}
            return render(request, 'orders/payments.html', context)
       
        
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('payment_id')

    try:
        order = OrderModel.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProductModel.objects.filter(order_id=order.id)
        payment = PaymentModel.objects.get(payment_id=transaction_id)
        
        sub_total = 0
        for i in ordered_products:
            sub_total += i.product_price * i.quantity

        context = {
            'order':order,
            'ordered_products': ordered_products,
            'order_number':order.order_number,
            'transactionID':payment.payment_id,
            'payment':payment,
            'sub_total':sub_total,
            'tax': order.tax,
            'grand_total': order.order_total,
        }
        return render(request, 'orders/order_complete.html', context)

    except (PaymentModel.DoesNotExist, OrderModel.DoesNotExist):
        return redirect('home')