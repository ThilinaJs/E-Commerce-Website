from itertools import product
from multiprocessing import context
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView, CreateView
from ecomapp.forms import CheckoutForm
from ecomapp.models import Cart, CartProduct, Category, Product
from .forms import CheckoutForm
from .models import *

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list']=Product.objects.all().order_by("-id")
        context['allcategories'] = Category.objects.all()
        return context

class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories']=Category.objects.all()
        return context

class ProductDetailView(TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count +=1
        product.save()
        context['product']= product
        return context

class AddToCartView(TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['pro_id']

        product_obj = Product.objects.get(id=product_id)

        cart_id = self.request.session.get("cart_id", None)

        if cart_id:

            cart_obj = Cart.objects.get(id=cart_id)

            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity +=1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate = product_obj.selling_price, quantity = 1, subtotal =product_obj.selling_price )
                cart_obj.total += product_obj.selling_price
                cart_obj.save()


        else:
            cart_obj = Cart.objects.create(total = 0)
            self.request.session['cart_id'] = cart_obj.id

            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate = product_obj.selling_price, quantity = 1, subtotal =product_obj.selling_price )
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context

class EmptyCartView(TemplateView):
    def get(self,request, *args, **kwargs):
        cart_id =request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total =0
            cart.save()
        return redirect('ecomapp:mycart')



class MyCartView(TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart']=cart
        return context
class CheckoutView(CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm 
    success_url = reverse_lazy('ecomapp:home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id= self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart']=cart_obj
        return context 

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')

        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect('ecomapp:home')
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contactus.html"

