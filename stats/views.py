from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from pyexpat.errors import messages

from .models import *

class SalesView(LoginRequiredMixin, View):
    login_url='login'

    def get(self, request):
        sales=Sale.objects.filter(branch=request.user.branch)
        products=Product.objects.filter(branch=request.user.branch)
        clients=Client.objects.filter(branch=request.user.branch)
        search = request.GET.get('search')
        if search:
            clients = clients.filter(
                Q(product__icontains=search) |
                Q(client__icontains=search)
            )
        context={
            'sales':sales,
            'products':products,
            'clients':clients,
            'search':search

        }
        return render(request, 'sales.html', context)


    def post(self, request):
        client = get_object_or_404(Client, id=request.POST['client_id'])
        product=get_object_or_404(Product, id=request.POST['product_id'])
        quantity = float(request.POST.get('quantity')) if request.POST.get('quantity')is not None else None
        total_price = float(request.POST.get('total_price')) if request.POST.get('total_price') is not None else None
        debt = float(request.POST.get('debt_price')) if request.POST.get('debt_price')is not None else None
        paid = float(request.POST.get('paid_price')) if request.POST.get('paid_price')is not None else None
        context=self.check_enough_product(self, product, quantity)
        if context is not None:
            return render(request, 'warning.html', context)

        if paid and debt:
            total_price=debt+paid

        if not total_price:
            total_price=product.price*quantity

        if not paid and not debt:
            paid=total_price

        if not debt and paid:
            debt=total_price-paid

        if not paid and debt:
            paid= total_price-debt

        Sale.objects.create(

            product=product,
            quantity=quantity,
            client=client,
            total_price=total_price,
            paid_price=paid,
            debt_price=debt,
            user=request.user,
            branch=request.user.branch
        )

        product.quantity -= quantity
        product.save()

        client.debt+=debt
        client.save()

        return redirect('sales')

    def check_enough_product(self, request,  product, quantity):
        if product.quantity < quantity:
            warning_message = f"{product.name} so'ralgan miqdorda mavjud emas! Mavju: {product.quantity} {product.unit}"
            warning_title = 'Mahsulot yetarli emas'
            back_url = 'sales'
            context = {
                'warning_message': warning_message,
                'warning_title': warning_title,
                'back_url': back_url
            }
            return context
        return None
def Sales_delete_view(request, id):
    sales = get_object_or_404(Sale,id=id)

    context={
        'sales':sales
    }
    if request.method == "POST":
        sales.delete()
        return redirect('sales')


    return render(request, "sales_confirm.html", context )




def Sales_update_view(request, pk):
    products=Product.objects.filter(branch=request.user.branch),
    clients=Client.objects.filter(branch=request.user.branch),
    sales = get_object_or_404(Sale, pk=pk)
    context={
        'products':products,
        'clients':clients,
        'sales':sales,
    }
    if request.method == "POST":
        sales.product =  get_object_or_404(Product,  name=request.POST['product'])
        sales.client =get_object_or_404(Client,  name=request.POST['client'])
        sales.quantity = request.POST.get('quantity')
        sales.total_price = request.POST.get('total_price')
        sales.paid_price = request.POST.get('paid_price')
        sales.debt_price = request.POST.get('debt_price')
        sales.save()
        return redirect('sales')

    return render(request, 'sales-edit.html', context)



class ImportProductsView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        import_products=importproduct.objects.filter(branch=request.user.branch).order_by('-created_at')
        products=Product.objects.filter(branch=request.user.branch)
        search = request.GET.get('search')
        if search:
            import_products =import_products.filter(
                Q(product__name__icontains=search)
            )
        context={
            'import_products':import_products,
            'products':products,
            'search':search
        }
        return render(request, 'import-products.html', context)

    def post(self, request):
        product=get_object_or_404(Product, id=request.POST['product_id'])
        quantity=float(request.POST.get('quantity')) if request.POST.get('quantity')is not None else None
        importproduct.objects.create(
            product=product,
            quantity=quantity,
            buy_price=request.POST.get('buy_price'),
            user=request.user,
            branch=request.user.branch
        )
        product.quantity+=quantity
        product.save()
        return redirect('imports')

def Imports_delete_view(request, id):
    importproducts = get_object_or_404(importproduct,id=id)

    context={
        'importproducts':importproducts
    }
    if request.method == "POST":
        importproducts.delete()
        return redirect('imports')


    return render(request, "imports_confirm.html", context )





class PaydebtsView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        pay_debts=PayDebt.objects.filter(branch=request.user.branch).order_by('-created_at')
        clients=Client.objects.filter(branch=request.user.branch).order_by('name')
        search = request.GET.get('search')
        if search:
            client= clients.filter(
                Q(name__icontains=search)
            )
        context={
            'pay_debts':pay_debts,
            'clients':clients
        }
        return render(request, 'pay_debts.html', context)

    def post(self, request):
        client=get_object_or_404(Client, id=request.POST.get('client_id'))
        price = float(request.POST.get('price')) if request.POST.get('price')is not None else None
        if price==0:
            return redirect('pay-debts')
        PayDebt.objects.create(
            client=client,
            price=price,
            description=request.POST.get('description'),
            user=request.user,
            branch=request.user.branch
        )
        client.debt-=price
        client.save()
        return redirect('pay-debt')

def Paydebt_delete_view(request, id):
    pay_debt = get_object_or_404(PayDebt,id=id)

    context={
        'pay_debt':pay_debt
    }
    if request.method == "POST":
        pay_debt.delete()
        return redirect('pay-debt')


    return render(request, "delete_confirm.html", context )

def Paydebt_edit_view(request, pk):
    pay_debts = PayDebt.objects.get(pk=pk, branch=request.user.branch)
    context={
        'pay_debts':pay_debts
    }
    if request.method == "POST":
        pay_debts.client = get_object_or_404(Client, name=request.POST['client'])
        pay_debts.price = request.POST.get('price')
        pay_debts.description = request.POST.get('description')
        pay_debts.save()
        return redirect('pay-debt')
    return render(request, 'pay_debts_edit.html', context)










