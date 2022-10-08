from django.shortcuts import render
from django.views.generic import TemplateView
from ecomapp.models import Category, Product

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list']=Product.objects.all()
        context['allcategories'] = Category.objects.all()
        return context

class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs
        )



class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contactus.html"

