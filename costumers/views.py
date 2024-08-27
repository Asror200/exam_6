import csv
import io
import openpyxl
import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from costumers.models import Customers
from costumers.forms import AddCustomerForm, SendEmailForm
from django.contrib import messages
from typing import Optional
from django.db.models import Q
from transliterate import translit
from django.core.paginator import Paginator
from django.views.generic import View, FormView, edit
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile


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


class CustomerDeleteView(edit.DeleteView):
    model = Customers
    template_name = 'costumers/delete-confirm-customer.html'
    success_url = reverse_lazy('home')
    slug_field = 'slug'
    slug_url_kwarg = '_slug'

    def form_valid(self, form):
        messages.success(self.request, 'Product deleted successfully')
        return super().form_valid(form)


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


class SendingEmail(FormView):
    form_class = SendEmailForm
    template_name = 'costumers/send-email.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        to_email = form.cleaned_data['to_email']
        message = form.cleaned_data['message']
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        messages.success(self.request, 'Your email has been sent.')
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Something went wrong, please try again')
        return response


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            return obj.url
        return super().default(obj)


class ExportDataView(View):
    def get(self, request, *args, **kwargs):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        format = request.GET.get('format')

        if format == 'csv':
            return self.export_csv(date)

        elif format == 'json':
            return self.export_json(date)

        elif format == 'xlsx':
            return self.export_xlsx(date)

        else:
            return HttpResponse('Bad Request', status=400)

    def export_csv(self, date):
        meta = Customers._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={Customers._meta.object_name}-{date}.csv'

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in Customers.objects.all():
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_json(self, date):
        response = HttpResponse(content_type='application/json')
        customers = Customers.objects.all()
        data = []

        for customer in customers:
            customer_dict = model_to_dict(customer)
            if 'image_field' in customer_dict:
                customer_dict['image_field'] = customer_dict['image_field'].url if customer_dict[
                    'image_field'] else None
            data.append(customer_dict)

        response.write(json.dumps(data, indent=4, cls=CustomJSONEncoder))
        response['Content-Disposition'] = f'attachment; filename=customers-{date}.json'

        return response

    def export_xlsx(self, date):
        customers = Customers.objects.all()
        meta = Customers._meta
        field_names = [field.name for field in meta.fields]
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Customers"
        worksheet.append(field_names)
        for customer in customers:
            row = []
            for field in field_names:
                value = getattr(customer, field)
                if hasattr(value, 'url'):
                    value = value.url
                elif isinstance(value, datetime.datetime):
                    if value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, datetime.date):
                    value = value.strftime('%Y-%m-%d')
                row.append(value)
            worksheet.append(row)
        virtual_workbook = io.BytesIO()
        workbook.save(virtual_workbook)
        virtual_workbook.seek(0)
        response = HttpResponse(content=virtual_workbook.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=customers-{date}.xlsx'
        return response


class CalendarView(View):
    """This class is used to calculate a calendar"""

    def get(self, request):
        return render(request, 'costumers/app/calendar.html')


class ShoppingCartListView(View):
    """This is currently only working by default"""

    def shopping_cart(self, request):
        return render(request, 'costumers/shopping-cart.html')
