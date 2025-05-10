from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from marketplace.context_processor import get_cart_amount, get_cart_counter
from marketplace.models import Cart
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q
#Geodjango
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listing.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories  = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'foodItems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'cart_items': cart_items,
        'vendor': vendor,
        'categories': categories
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exists
            try:
                fooditem = FoodItem.objects.get(pk=food_id)
                #check if the user has alredy added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, foodItem=fooditem)
                    print("sono qui")
                    #Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'increase the cart quantity', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': chkCart.quantity,
                        'cart_amount': get_cart_amount(request)
                        })
                except Cart.DoesNotExist:
                    chkCart = Cart.objects.create(user=request.user, foodItem=fooditem, quantity=1)
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Added the food to the cart', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': chkCart.quantity,
                        'cart_amount': get_cart_amount(request)
                        })
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})

def remove_from_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exists
            try:
                fooditem = FoodItem.objects.get(pk=food_id)
                #check if the user has alredy added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, foodItem=fooditem)
                    #Decrease the cart quantity
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'decrease the cart quantity', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': chkCart.quantity,
                        'cart_amount': get_cart_amount(request)
                        })
                except Cart.DoesNotExist:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart'})
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    for item in cart_items:
        print(item.foodItem.id)
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #check if the cart items exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Cart item has been deleted', 
                        'cart_counter': get_cart_counter(request),
                        'cart_amount': get_cart_amount(request)
                        })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'cart Item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
        
def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address']
        lat = request.GET['lat']
        lng = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']

        #get vendor ids that has the foo item the user is looking for
        fetch_vendors_by_fooditems = FoodItem.objects.filter(
            food_title__icontains=keyword, 
            is_available=True
        ).values_list('vendor', flat=True)
        vendors = Vendor.objects.filter(
            Q(
                id__in=fetch_vendors_by_fooditems
            ) | 
            Q(
                vendor_name__icontains=keyword, 
                is_approved=True, 
                user__is_active=True)
        )
        if lat and lng and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (lng, lat))
            vendors = Vendor.objects.filter(
                Q(
                id__in=fetch_vendors_by_fooditems
            ) | 
            Q(
                vendor_name__icontains=keyword, 
                is_approved=True, 
                user__is_active=True),
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)
        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
            'source_location': address
        }
        return render(request, 'marketplace/listing.html', context)
