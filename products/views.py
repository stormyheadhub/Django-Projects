from gc import get_objects
from lib2to3.fixes.fix_input import context

from django.core.signals import request_started
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import ProductForm
from .models import Product

def admin_console(request):
    products = Product.objects.all()
    return render(request, 'products/products_page.html', ('products':products))

def details(request, pk):
    pk = int(pk)
    item = get_object_or_404(Product, pk=pk)
    form = ProductForm(data=request.POST or None, instance=item)
    if request.method == 'POST':
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.save ()
            return redirect('admin_console')
        else:
            print(form.errors)
    else:
        return render(request, 'products/present_product.html', {'form': form})

def delete(request, pk):
    pk = int(pk)
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('admin_console')
    context = {'item': item}
    return render(request, "products/confirmDelete.html", context)

def confirm(request):
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.delete()
            return redirect('admin_console')
    else:
        return redirect('admin_console')

def createRecord(request):
    form = ProductForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_console')
    else:
        print(form.errors)
        form = ProductForm()
    context = {
        'form': form,
    }
return render(request_started, 'products/createRecord.html', context)
