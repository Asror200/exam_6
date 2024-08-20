from django.shortcuts import render, redirect, get_object_or_404
from costumers.models import Customers
from costumers.forms import AddCustomerForm
from django.contrib import messages
from typing import Optional
from django.db.models import Q
from transliterate import translit
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import View


# Create your views here.


class CustomerListView(View):
    def get(self, request, _slug: Optional[str] = None):
        """This function is the home view and shows all customers."""
        search = request.GET.get('search')
        filter_type = request.GET.get('filter', '')
        customers = Customers.objects.all().order_by('created_at')
        if filter_type:
            customers = customers.order_by('-created_at')
        if search:
            """This is to convert requests sent in Cyrillic to Latin"""
            latin = translit(search, 'ru', reversed=True)
            customers = customers.filter(
                Q(first_name__icontains=latin) |
                Q(last_name__icontains=latin) |
                Q(email__icontains=latin)
            )
        page = request.GET.get('page')
        paginator = Paginator(customers, 5)
        page_obj = paginator.get_page(page)
        context = {
            'customers': page_obj,
        }
        return render(request, 'costumers/customers.html', context)


class CustomerDetailView(View):
    def get(self, request, _slug: Optional[str] = None):
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


class CustomerUpdateView(View):
    """This class is used to edit a customer."""

    def get(self, request, _slug):
        customer = get_object_or_404(Customers, slug=_slug)
        form = AddCustomerForm(instance=customer)
        context = {
            'form': form,
        }
        return render(request, 'costumers/add-customer.html', context)

    def post(self, request, _slug):
        customer = get_object_or_404(Customers, slug=_slug)
        form = AddCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your customer has been saved.')
            return redirect('customer_details', _slug)
        messages.error(request, 'Something went wrong. Please try again.')
        return redirect('edit_customer', _slug)


class CustomerDeleteView(View):
    """This class deletes a customer from the database."""

    def get(self, request, _slug):
        customer = get_object_or_404(Customers, slug=_slug)
        customer.delete()
        messages.success(request, 'Your customer has been deleted.')
        return redirect('home')


class CustomerCreateView(View):
    """this class is used to add a customer"""

    def get(self, request):
        form = AddCustomerForm()

        return render(request, 'costumers/add-customer.html', {'form': form})

    def post(self, request):
        form = AddCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your customer has been saved.')
            return redirect('home')
        messages.error(request, 'Something went wrong. Please try again.')
        return redirect('add_customer')


class CalendarView(View):
    """This class is used to calculate a calendar"""

    def get(self, request):
        return render(request, 'costumers/app/calendar.html')


class ShoppingCartListView(View):
    """This is currently only working by default"""
    def shopping_cart(self, request):
        return render(request, 'costumers/shopping-cart.html')