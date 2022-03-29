from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from cart.models import CartItemModel, CartModel
from store.models import Product, VariationModel

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required


def _cart_id(request):
    # get the cart id from session cookies
    cart_id = request.session.session_key

    # if there's no cart id then create one
    if not cart_id:
        cart_id = request.session.create()

    return cart_id


# Create your views here.

# @login_required
def add_to_cart(request, product_id):
    current_user = request.user
# getting product here
    product = Product.objects.get(id=product_id)  # to get the product

# if user if authenticated
    if current_user.is_authenticated:
        # getting product variation
        product_variation = []

        if request.method == 'POST':

            # looping through whatever we get from request.POST, if we select black color then key = color and value = black
            for item in request.POST:
                key = item
                value = request.POST[key]
                # print(key, value)

                # check these key and values match with the ones in model admin order
                try:
                    variation = VariationModel.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)

                except:
                    pass

   
    # getting cart item here

        is_cart_item_exists = CartItemModel.objects.filter(
            product=product, user=current_user).exists()

        # first check whether the item with that variation already exists in the cart, if yes just increment the quantity, else create a new item
        if is_cart_item_exists:
            # get the product from the cart object
            cart_item = CartItemModel.objects.filter(
                product=product, user=current_user)

            # existing variation -> from database
            # current variation -> from product_variation list
            #  item_id -> database

            # check if current variation is in existing variation
            existing_variation_list = []
            id_list = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id_list.append(item.id)

            # print(existing_variation_list)

            # checking if current variation is present in variation in database or not
            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItemModel.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # update a new cart item
                item = CartItemModel.objects.create(
                    product=product, quantity=1, user=current_user)
                # if length of the list is empty then  just update the quantity else add the item inside database
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()

        else:
            # if user is not authenticated
            cart_item = CartItemModel.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect('cart')

    else:
        # getting product variation
        product_variation = []

        if request.method == 'POST':

            # looping through whatever we get from request.POST, if we select black color then key = color and value = black
            for item in request.POST:
                key = item
                value = request.POST[key]
                # print(key, value)

                # check these key and values match with the ones in model admin order
                try:
                    variation = VariationModel.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)

                except:
                    pass

    # getting cart here
        try:
            # get the cart using cart_id present in the session
            cart = CartModel.objects.get(cart_id=_cart_id(request))

        # if cart doesnt exist then create a new cart by cart id
        except CartModel.DoesNotExist:
            cart = CartModel.objects.create(
                cart_id=_cart_id(request),
            )

        cart.save()

    # getting cart item here

        is_cart_item_exists = CartItemModel.objects.filter(
            product=product, cart=cart).exists()

        # first check whether the item with that variation already exists in the cart, if yes just increment the quantity, else create a new item
        if is_cart_item_exists:
            # get the product from the cart object
            cart_item = CartItemModel.objects.filter(
                product=product, cart=cart)

            # existing variation -> from database
            # current variation -> from product_variation list
            #  item_id -> database

            # check if current variation is in existing variation
            existing_variation_list = []
            id_list = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id_list.append(item.id)

            print(existing_variation_list)

            # checking if current variation is present in variation in database or not
            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItemModel.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # update a new cart item
                item = CartItemModel.objects.create(
                    product=product, quantity=1, cart=cart)
                # if length of the list is empty then  just update the quantity else add the item inside database
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()

        else:
            cart_item = CartItemModel.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect('cart')


# @login_required
def remove_from_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItemModel.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = CartModel.objects.get(cart_id=_cart_id(request))
            cart_item = CartItemModel.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')


# @login_required
def delete_from_cart(request, product_id, cart_item_id):
   
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItemModel.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = CartModel.objects.get(cart_id=_cart_id(request))
        cart_item = CartItemModel.objects.get(product=product, cart=cart, id=cart_item_id)
        
    cart_item.delete()
    return redirect('cart')


# @login_required
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

    # if user is logged in then get the cart item by user
        if request.user.is_authenticated:
            cart_items = CartItemModel.objects.filter(
                user=request.user, is_active=True)
        else:
            # first get the cart by cart id
            cart = CartModel.objects.get(cart_id=_cart_id(request))
            cart_items = CartItemModel.objects.filter(
                cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.discounted_price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass

    context = {'total': total, 'quantity': quantity,
               'cart_items': cart_items, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'cart.html', context)


@login_required(login_url="login")
def checkout(request, tax=0, total=0, grand_total=0, quantity=0, cart_items=None):
    try:
        # first get the cart by cart id
        if request.user.is_authenticated:
            cart_items = CartItemModel.objects.filter(
                user=request.user, is_active=True)
        else:
            # first get the cart by cart id
            cart = CartModel.objects.get(cart_id=_cart_id(request))
            cart_items = CartItemModel.objects.filter(
                cart=cart, is_active=True)
                
        for cart_item in cart_items:
            total += (cart_item.product.discounted_price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass

    context = {'total': total, 'quantity': quantity,
               'cart_items': cart_items, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'checkout.html', context)
