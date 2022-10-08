from django.shortcuts import render
from django.views.generic import TemplateView
from ecomapp.models import Category, Product

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

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contactus.html"

