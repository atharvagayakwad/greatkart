from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import CartItemModel
from cart.views import _cart_id

from category.models import CategoryModel
from orders.models import OrderProductModel
from store.forms import ReviewForm
from store.models import Product, ReviewRatingModel

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages

def store(request, category_slug=None):
    categories = None
    products = None

# if a slug is found then find which category relates to that slug and get the product acc to the category
    if category_slug != None:
        categories = get_object_or_404(CategoryModel, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')  # here we're doing ?page=2
        paged_products = paginator.get_page(page)
        product_count = products.count()

# otherwise display all products
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')  # here we're doing ?page=2
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {'products': paged_products, 'product_count': product_count, }
    return render(request, 'store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        # category__slug means we are accessing category from Product Model and then accessing slug of that category present in CategoryModel
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        already_in_cart = CartItemModel.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            # in order to show submit review button check whether product is already bought by user
            order_product = OrderProductModel.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProductModel.DoesNotExist: 
            order_product = None
    else:
        order_product = None
        
    # get the Reviews
    reviews = ReviewRatingModel.objects.filter(product_id=single_product.id, status=True)
    
    context = {'single_product': single_product,
               'already_in_cart': already_in_cart, 'order_product':order_product, 'reviews':reviews}
    return render(request, 'product_detail.html', context)


def search(request):
    # first check that the get request has ?keyword= or not
    if 'keyword' in request.GET:
        # if yes then store the value of that keyword in keyword var
        keyword = request.GET['keyword']

# if keyword exists then check whether whether that product_name has a word that matches with the keyword, if yes show the results
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(product_name__icontains=keyword)
            product_count = products.count()

    context = {'products': products, 'product_count': product_count}
    return render(request, 'store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER') # current url will be stored here

    if request.method == 'POST':
        try:
            # check if there already exists a review, if yes then update it
            reviews = ReviewRatingModel.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews) # instance is used here to check if there exists any previous reviews
            form.save()
            messages.success(request,'Thank you! Your review has been updated!')
            return redirect(url)
        except ReviewRatingModel.DoesNotExist:
            # else create a new review
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRatingModel()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Your review has been submitted')
                return redirect(url)
