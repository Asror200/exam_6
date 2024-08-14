from django.shortcuts import render, redirect, get_object_or_404
from costumers.models import Customers
from costumers.forms import AddCustomerForm
from django.contrib import messages
from typing import Optional
from django.db.models import Q
from transliterate import translit
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request, _slug: Optional[str] = None):
    """This function is the home view and shows all customers."""
    customers = Customers.objects.all()
    search = request.GET.get('search')
    filter_type = request.GET.get('filter', '')
    if filter_type:
        customers = Customers.objects.all().order_by('-created_at')
    if search:
        """This is to convert requests sent in Cyrillic to Latin"""
        latin = translit(search, 'ru', reversed=True)

        customers = Customers.objects.filter(Q(first_name__icontains=latin) |
                                             Q(last_name__icontains=latin) |
                                             Q(email__icontains=latin))
    context = {
        'customers': customers,
    }
    return render(request, 'costumers/customers.html', context)


def customer_detail(request, _slug: Optional[str] = None):
    """This function is used to display a customer detail page."""
    customer = get_object_or_404(Customers, slug=_slug)
    search = request.GET.get('search')
    if search:
        """This is to convert requests sent in Cyrillic to Latin"""
        latin = translit(search, 'ru', reversed=True)

        customers = Customers.objects.filter(Q(first_name__icontains=latin) |
                                             Q(last_name__icontains=latin) |
                                             Q(email__icontains=latin))
        return render(request, 'costumers/customers.html', {'customers': customers})
    context = {
        'customer': customer
    }
    return render(request, 'costumers/customer-details.html', context)


@login_required(login_url='login_page')
def edit_customer(request, _slug):
    """This function is used to edit a customer."""
    customer = get_object_or_404(Customers, slug=_slug)
    form = AddCustomerForm(instance=customer)
    if request.method == 'POST':
        form = AddCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your customer has been saved.')
            return redirect('customer_details', _slug)
        messages.error(request, 'Something went wrong. Please try again.')
        return redirect('edit_customer', _slug)
    context = {
        'form': form,
    }
    return render(request, 'costumers/add-customer.html', context)


@login_required(login_url='login_page')
def delete_customer(request, _slug):
    """This function deletes a customer from the database."""
    customer = get_object_or_404(Customers, slug=_slug)
    customer.delete()
    messages.success(request, 'Your customer has been deleted.')
    return redirect('home')


@login_required(login_url='login_page')
def add_customer(request):
    """this function is used to add a customer"""
    form = AddCustomerForm()
    if request.method == 'POST':
        form = AddCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your customer has been saved.')
            return redirect('home')
        messages.error(request, 'Something went wrong. Please try again.')
        return redirect('add_customer')
    return render(request, 'costumers/add-customer.html', {'form': form})


def calendar(request):
    """This function is used to calculate a calendar"""
    return render(request, 'costumers/app/calendar.html')


def shopping_cart(request):
    """This is currently only working by default"""
    return render(request, 'costumers/shopping-cart.html')
