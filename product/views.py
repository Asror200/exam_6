from django.contrib import messages
from product.models import Product, ProductAttribute
from django.views.generic import edit, detail, list
from product.forms import ProductModelForm, ProductForm
from django.urls import reverse_lazy


# Create your views here.


class ProductListView(list.ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        pictures = {}
        for product in page_obj.object_list:
            if product.images.exists():
                pictures[product.id] = product.images.first().image.url
        context['pictures'] = pictures
        return context

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        new_arrived = self.request.GET.get('filter')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        if new_arrived:
            return Product.objects.all().order_by('-created_at')
        return Product.objects.all()


class ProductGribView(list.ListView):
    model = Product
    template_name = 'product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        pictures = {}
        for product in page_obj.object_list:
            if product.images.exists():
                pictures[product.id] = product.images.first().image.url
        context['pictures'] = pictures
        return context

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        new_arrived = self.request.GET.get('filter')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        if new_arrived:
            return Product.objects.all().order_by('-created_at')
        return Product.objects.all()


class ProductDetailView(detail.DetailView):
    model = Product
    template_name = 'product/product-details.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = '_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['main_image'] = product.images.first()
        context['other_images'] = product.images.exclude(id=context['main_image'].id) if context[
            'main_image'] else product.images.all()
        context['product_attributes'] = ProductAttribute.objects.filter(product=product)
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

    def get_queryset(self):
        return Product.objects.all()
