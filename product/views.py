from django.contrib import messages
from django.shortcuts import redirect
from product.models import Product
from django.views.generic import edit, detail, list
from product.forms import ProductModelForm, ProductForm, ProductCommitForm
from django.urls import reverse_lazy
from django.db.models import Avg


# Create your views here.


class ProductListView(list.ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        new_arrived = self.request.GET.get('filter')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        if new_arrived:
            return Product.objects.all().order_by('-created_at')
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            average_rating = product.commit_set.aggregate(average_rating=Avg('rating'))['average_rating'] or 0
            product.average_rating = average_rating
        return context


class ProductGribView(list.ListView):
    model = Product
    template_name = 'product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        new_arrived = self.request.GET.get('filter')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        if new_arrived:
            return Product.objects.all().order_by('-created_at')
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()

        for product in products:
            product.average_rating = product.commit_set.aggregate(
                average_rating=Avg('rating')
            )['average_rating'] or 0

        context['products'] = products
        return context


class ProductDetailView(detail.DetailView):
    model = Product
    template_name = 'product/product-details.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = '_slug'

    def post(self, request, *args, **kwargs):
        form = ProductCommitForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.product = self.get_object()
            commit.save()
            messages.success(request, 'Your commit has been saved.')
            return redirect('product_detail', _slug=self.get_object().slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        commits = product.commit_set.order_by('-rating')[:3]
        average_rating = product.commit_set.aggregate(average_rating=Avg('rating'))['average_rating'] or 0
        context['average_rating'] = average_rating

        context['commits'] = commits
        return context


class ProductAddView(edit.CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'product/add-product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product added successfully')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Something went wrong, please try again')
        return response


class ProductUpdateView(edit.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/add-product.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'_slug': self.object.slug})

    def get_object(self, queryset=None):
        _slug = self.kwargs.get('_slug')
        return Product.objects.get(slug=_slug)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product updated successfully')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong, please try again')
        return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(edit.DeleteView):
    model = Product
    template_name = 'product/delete_confirm_product.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Product deleted successfully')
        return super().form_valid(form)
