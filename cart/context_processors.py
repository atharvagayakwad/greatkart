from cart.views import _cart_id
from .models import CartModel, CartItemModel

def counter(request):
    cart_count = 0
    try:      
        cart = CartModel.objects.filter(cart_id=_cart_id(request))

        # if user is logged in then give cart item count of that particular user
        if request.user.is_authenticated:
            cart_items= CartItemModel.objects.all().filter(user=request.user)
        
        else:
            cart_items= CartItemModel.objects.filter(cart=cart[:1])
        
        for cart_item in cart_items:
            cart_count += cart_item.quantity
            
    except CartModel.DoesNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)