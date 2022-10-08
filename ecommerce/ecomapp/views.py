from itertools import product
from multiprocessing import context
from django.shortcuts import render
from django.views.generic import TemplateView
from ecomapp.models import Cart, CartProduct, Category, Product

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

            cart_obj = Cart.objects.create(total=0)

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

        return context




class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contactus.html"

