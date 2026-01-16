from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import product, Contact, Orders
from math import ceil   
import json
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def index(request):
    allprods = []
    cats = product.objects.values_list('category', flat=True).distinct()

    for cat in cats:
        prods = product.objects.filter(category=cat)
        nSlides = ceil(len(prods) / 4)
        chunks = [prods[i*4:(i+1)*4] for i in range(nSlides)]
        allprods.append([cat, chunks])

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'shop/index.html', {
        'allprods': allprods,
        'cart_count': cart_count
    })

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        email = request.POST.get("email")

        try:
            order = Orders.objects.get(order_id=order_id, email=email)

            try:
                cart = json.loads(order.items_json)
            except:
                cart = {}

            items = []

            # 🔥 IMPORTANT CHANGE: key = product_name
            for product_name, qty in cart.items():
                try:
                    prod = product.objects.get(product_name=product_name)

                    quantity = qty[0] if isinstance(qty, list) else qty

                    items.append({
                        "name": prod.product_name,
                        "quantity": quantity,
                        "price": prod.price
                    })

                except product.DoesNotExist:
                    continue

            return JsonResponse({
                "status": "success",
                "order_id": order.order_id,
                "amount": order.amount,
                "status_desc": "Order Placed",
                "items": items
            })

        except Orders.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Order not found"
            })

    return render(request, "shop/tracker.html")

def productview(request, id):
    prod = product.objects.get(product_id=id)
    return render(request,'shop/prodviews.html', {'product': prod})



client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for name, qty in cart.items():
        try:
            prod = product.objects.get(product_name=name)
            subtotal = prod.price * qty
            total += subtotal

            items.append({
                'product': prod,
                'quantity': qty,
                'subtotal': subtotal
            })
        except product.DoesNotExist:
            continue

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        amount_paise = total * 100

        razorpay_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        Orders.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            address=request.POST.get('address'),
            items_json=json.dumps(cart),
            amount=total,
            razorpay_order_id=razorpay_order["id"]
        )

        return JsonResponse({
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order["id"],
            "amount": amount_paise
        })

    return render(request, "shop/checkout.html", {
        'items': items,
        'total': total
    })


def remove_from_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pid = data.get("product_id")

        cart = request.session.get("cart", {})

        try:
            prod = product.objects.get(product_id=pid)
            item_name = prod.product_name
        except product.DoesNotExist:
            return JsonResponse({'success': False})

        if item_name in cart:
            del cart[item_name]
            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({'success': True})


def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = product.objects.filter(product_name__icontains=query)
    return render(request, 'shop/search_results.html', {'results': results, 'query': query})
    #return render(request, 'shop/search.html')

@csrf_protect
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id', '')).strip()
        quantity = int(data.get('quantity', 0))

        # ❌ BLOCK INVALID DATA
        if not product_id.isdigit() or quantity <= 0:
            return JsonResponse({'success': False})

        # 🔹 GET PRODUCT NAME
        try:
            prod = product.objects.get(product_id=int(product_id))
            item_name = prod.product_name
        except product.DoesNotExist:
            return JsonResponse({'success': False})

        # 🔹 GET CART FROM SESSION
        cart = request.session.get('cart', {})

        # ✅ STORE BY ITEM NAME INSTEAD OF ID
        cart[item_name] = cart.get(item_name, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'cart_count': sum(cart.values())
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def home(request):
    allprods = []
    catprods = product.objects.values('category', 'product_id')

    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = ceil(n / 4)
        chunks = [prod[i:i+4] for i in range(0, n, 4)]
        allprods.append([cat, chunks])

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'shop/index.html', {
        'allprods': allprods,
        'cart_count': cart_count
    })

@require_POST
def remove_from_cart(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')

    cart = request.session.get('cart', {})

    # Find product by id
    try:
        prod = product.objects.get(product_id=product_id)
        item_name = prod.product_name
        if item_name in cart:
            del cart[item_name]
            request.session['cart'] = cart
            request.session.modified = True
    except product.DoesNotExist:
        pass

    total = 0
    for name, qty in cart.items():
        try:
            prod = product.objects.get(product_name=name)
            total += prod.price * qty
        except product.DoesNotExist:
            pass

    return JsonResponse({
        'success': True,
        'cart_count': sum(cart.values()),
        'total': total
    })

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')

        order = Orders.objects.get(id=order_id)
        order.payment_status = "Paid"
        order.razorpay_payment_id = payment_id
        order.save()

        return JsonResponse({'status': 'success'})
    
def clear_cart(request):
    if request.method == "POST":
        request.session['cart'] = {}
        request.session.modified = True
        return JsonResponse({"success": True})