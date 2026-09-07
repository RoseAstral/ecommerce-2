from django.shortcuts import render, redirect, get_object_or_404
from .form import RegisterForm, LoginUserForm, StoreForm, ProductForm, ReviewForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .models import Store, Product, Review, RestToken, StoreSerializer, ProductSerializer, ReviewSerializer
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from django.contrib import messages
import secrets
from hashlib import sha1
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def setup_groups_and_Permissions():
        Vendors, created = Group.objects.get_or_create(name='Vendors')
        group1 = Group.objects.get(name="Vendors")
        content_type1 = ContentType.objects.filter(app_label='store',
                                                 model__in=['Store', 'Product', 'Review'])
        perms1 = Permission.objects.filter(content_type__in=content_type1)
        group1.permissions.add(*perms1)
        Buyers, created = Group.objects.get_or_create(name='Buyers')
        group2 = Group.objects.get(name='Buyers')
        content_type2 = ContentType.objects.filter(app_label='store', 
                                           model__in=['Review'])
        perms2 = Permission.objects.filter(content_type__in=content_type2)
        group2.permissions.add(*perms2)

def frontpage(request):
    setup_groups_and_Permissions()
    store_list = Store.objects.all()
    product_list = Product.objects.all()
    cart_products = retreive_porducts(request)
    context = {'store_list': store_list,
               'product_list': product_list,
               'cart_products': cart_products,}
    return render(request, 'store/frontpage.html', context)

def buyer_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            my_group = Group.objects.get(name='Buyers')
            new_user = form.save(commit=False)
            new_user.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            my_group.user_set.add(request.user)
            return redirect('frontpage')
    else:
        form = RegisterForm()
    return render(request, "store/register_buyer.html", {'form': form})

def vender_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            my_group = Group.objects.get(name='Vendors')
            new_user = form.save(commit=False)
            new_user.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            my_group.user_set.add(request.user)
            return redirect('frontpage')
    else:
        form = RegisterForm()
    return render(request, "store/register_Vender.html", {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if request.user.is_authenticated:
                    logout(request)
                login(request, user)
                return HttpResponseRedirect(reverse('frontpage'))
    else:
        form = LoginUserForm()
    return render(request, "store/login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('frontpage')

def add_store_view(request):
    user = request.user
    if user.has_perm('store.add_store'):
        if request.method == "POST":
            form = StoreForm(request.POST)
            if form.is_valid():
                store = form.save(commit=False)
                store.owner = request.user
                store.save()
                return redirect("store:frontpage")
        else:
            form = StoreForm()
        return render(request, "store/add_store.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('frontpage'))
        

def update_store_view(request, pk):
    user = request.user
    if user.has_perm('store.change_store'):
        store = get_object_or_404(Store, pk=pk)
        if request.method == "POST":
            form = StoreForm(request.POST, instance=store)
            if form.is_valid():
                store = form.save(commit=False)
                store.save()
                return redirect("store:frontpage")
        else:
            form = StoreForm(instance=store)
        return render(request, "store/add_store.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('frontpage'))

def delete_store_view(request, pk):
    user = request.user
    if user.has_perm('store.delete_store'):
        post = get_object_or_404(Store, pk=pk)
        post.delete()
        return redirect("store:frontpage")
    else:
        return HttpResponseRedirect(reverse('frontpage'))

def add_product_view(request, pk):
    user = request.user
    if user.has_perm('store.add_product'):
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.store = Store.objects.get(pk=pk)
                product.seller = request.user
                product.save()
                return redirect("frontpage")
        else:
            form = ProductForm()
        return render(request, "store/add_product.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('frontpage'))

def update_product_view(request, pk):
    user = request.user
    if user.has_perm('store.change_product'):
        product = get_object_or_404(Product, pk=pk)
        if request.method == "POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                product = form.save(commit=False)
                product.save()
                return redirect("store:frontpage")
        else:
            form = ProductForm(instance=product)
        return render(request, "store/add_product.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('frontpage'))

def delete_product_view(request, pk):
    user = request.user
    if user.has_perm('store.delete_product'):
        post = get_object_or_404(Product, pk=pk)
        post.delete()
        return redirect("frontpage")
    else:
        return HttpResponseRedirect(reverse('store:frontpage'))

def store_details_view(request, pk):
    store_list = Store.objects.all()
    product_list = Product.objects.all()
    store = get_object_or_404(Store, pk=pk)
    filtered_products = Product.objects.filter(store=store)
    context = {'store_list': store_list,
               'product_list': product_list,
               'store': store,
               'filtered_products': filtered_products}
    return render(request, "store/store_details.html", context)

def product_details_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    review_list = Review.objects.filter(product=product)
    context = {'product': product, 'review_list': review_list}
    return render(request, "store/product_details.html", context)

def add_review_view(request, pk):
    product = Product.objects.get(pk=pk)
    user = request.user
    if user.has_perm('store.add_review'):
        if Review.objects.filter(product=product, writer=request.user).exists():
            messages.warning(request, "You cannot review a product more than once.")
            return redirect('product_details', pk=pk)
        if request.method == "POST":
            form=ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.writer = user
                review.product = Product.objects.get(pk=pk)
                review.save()
                messages.success(request, "Your review has been posted successfully.")
                return redirect('product_details', pk=pk)
        else:
            form = ReviewForm()
    else:
        messages.warning(request, "You do not have permission to post Reviews.")
        return redirect('store/product_details.html', pk=pk)
    return render(request, 'store/add_comment.html', {'product' : product, 'form' : form})

def add_item_to_cart_view(request, pk): 
    session = request.session
    item = get_object_or_404(Product, pk=pk)
    item_s = item.pk
    if 'cart' not in request.session:
        session['cart'] = [item_s]
    else:
        saved_list = session['cart']
        saved_list.append(item_s)
        session['cart'] = saved_list
    return redirect("frontpage")

def retreive_porducts(request):
    session = request.session
    product_pk = session.get('cart', [])
    products = Product.objects.filter(pk__in=product_pk)
    return products
            
def view_cart_view(request):
    cart = retreive_porducts(request)
    return render(request, 'store/cart.html', {'cart': cart})

def build_invoice(user, request):
    my_user = request.user
    subject = "Ecommerece Invoice"
    user_email = my_user.email
    domain_email = settings.DEFAULT_FROM_EMAIL
    body = f"Hi {my_user.username}, \nThank you for your purchase"
    email = EmailMessage(subject, body, domain_email, [user_email])
    return email

def send_invoice(request):
    if request.user.is_authenticated:
        session = request.session
        user_email = User.email
        email = build_invoice(user_email, request)
        email.send()
        session['cart'] = []
        return HttpResponseRedirect(reverse('frontpage'))
    else:
        messages.error(request, "You must be logged in before you can make a purchase.")
        return HttpResponseRedirect(reverse('view_cart'))

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_store_api_view(request): 
    if request.method == "POST":
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def view_store_api_view(request):
    if request.method == "GET":
        serializer = StoreSerializer(Store.objects.all(), many=True)
        return JsonResponse(data=serializer.data, safe=False)
    
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_product_api_view(request): 
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def view_product_api_view(request):
    if request.method == "GET":
        serializer = ProductSerializer(Product.objects.all(), many=True)
        return JsonResponse(data=serializer.data, safe=False)
    
@api_view(['GET'])
def view_review_api_view(request):
    if request.method == "GET":
        serializer = ReviewSerializer(Review.objects.all(), many=True)
        return JsonResponse(data=serializer.data, safe=False)
