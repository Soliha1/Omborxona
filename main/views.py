from itertools import product
from urllib import request

from django.db.models import ExpressionWrapper, F, FloatField, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import *


class SectionsView(LoginRequiredMixin ,View):
    login_url = 'login'
    def get(self, request):
        return render(request, 'sections.html')


class ProductsView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        products=Product.objects.filter(branch=request.user.branch).annotate(
            total=ExpressionWrapper(
                F('quantity')*F('price'),
                output_field=FloatField()
            )
        ).order_by('-total')
        search = request.GET.get('search')
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(brand__icontains=search)
            )

        context={
            'products':products,
            'branch':request.user.branch,
            'search':search
        }
        return render(request, 'products.html', context)
    def post(self, request):
        if request.user.branch is None:
            return redirect('products')
        Product.objects.create(
            name=request.POST.get('name'),
            brand = request.POST.get('brand'),
            price=request.POST.get('price'),
            quantity=request.POST.get('quantity'),
            unit=request.POST.get('unit'),
            branch=request.user.branch
        )
        return redirect('products')


def Products_delete_view(request, id):
    products = get_object_or_404(Product, id=id)

    context = {
        'products': products
    }
    if request.method == "POST":
        products.delete()
        return redirect('products')

    return render(request, "products_confirm.html", context)



class ProductUpdateView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request, pk):
        product=get_object_or_404(Product, pk=pk)
        context={
            'product':product
        }
        return render(request, 'mahsulot-tahrirlash.html', context)

    def post(self, request, pk):
        product=get_object_or_404(Product, pk=pk)
        product.name=request.POST.get('name')
        product.brand = request.POST.get('brand')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.unit = request.POST.get('unit')
        product.save()
        return redirect('products')


class ClientsView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        clients=Client.objects.all()
        search = request.GET.get('search')
        if search:
            clients = clients.filter(
                Q(name__icontains=search) |
                Q(shop_name__icontains=search)
            )
        context={
            'clients':clients
        }


        return render(request, 'mijozlar.html', context)
    def post(self, request):
        Client.objects.create(
            name=request.POST.get('name'),
            shop_name=request.POST.get('shop_name'),
            phone_number=request.POST.get('phone_number'),
            address=request.POST.get('address'),
            debt=request.POST.get('debt'),
            branch=request.user.branch if request.user and request.user.branch else None
        )
        return redirect('clients')


def Client_update_view(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.name = request.POST.get('name')
        client.shop_name = request.POST.get('shop_name')
        client.phone_number = request.POST.get('phone_number')
        client.address = request.POST.get('address')
        client.save()
        return redirect('clients')

    return render(request, 'mijoz-tahrirlash.html', {'client': client})


def Clients_delete_view(request, id):
    clients = get_object_or_404(Client, id=id)

    context = {
        'clients': clients
    }
    if request.method == "POST":
        clients.delete()
        return redirect('clients')

    return render(request, "clients_confirm.html", context)

