from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import ProductForm, ReviewProductForm
from .models import Product, Review


class IndexView(ListView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    model = Product
    ordering = ['name']


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'product/create_product.html'
    model = Product
    form_class = ProductForm
    permission_required = 'webapp.add_product'
    permission_denied_message = "Доступ запрещён"

    def get_success_url(self):
        return reverse('webapp:index')


class ProjectDetailView(DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    context_key = 'product'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    class_form = ProductForm
    template_name = 'product/update_product.html'
    context_object_name = 'product'
    fields = ['name', 'category', 'description', 'photo']
    permission_required = 'webapp.change_product'
    permission_denied_message = "Доступ запрещён"

    def get_success_url(self):
        return reverse('webapp:index')


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'
    permission_denied_message = "Доступ запрещён"


class AddReviewProduct(LoginRequiredMixin, CreateView):
    template_name = 'review/create_review.html'
    form_class = ReviewProductForm
    context_object_name = 'product'

    def form_valid(self, form):
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        product.reviews.create(author=self.request.user, product=product_pk, **form.cleaned_data)
        return redirect('webapp:detail_product', pk=product_pk)


class UpdateReviewProduct(UserPassesTestMixin, UpdateView):
    model = Review
    class_form = ReviewProductForm
    template_name = 'review/update_review.html'
    context_object_name = 'product'
    fields = ['description', 'rating']
    permission_required = 'webapp.change_review'
    permission_denied_message = "Доступ запрещён"

    def test_func(self):
        review_pk = self.kwargs.get('pk')
        review = Review.objects.get(pk=review_pk)
        return self.request.user == review.author or self.request.user.has_perm('webapp.change_review')

    def get_success_url(self):
        return reverse('webapp:detail_product', kwargs={'pk': self.object.product.pk})


class DeleteReviewProduct(UserPassesTestMixin, DeleteView):
    model = Review
    permission_required = 'webapp.delete_review'
    permission_denied_message = "Доступ запрещён"

    def test_func(self):
        review_pk = self.kwargs.get('pk')
        review = Review.objects.get(pk=review_pk)
        return self.request.user == review.author or self.request.user.has_perm('webapp.change_review')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:detail_product', kwargs={'pk': self.object.product.pk})
