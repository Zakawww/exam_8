from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/create/', views.ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>/', views.ProjectDetailView.as_view(), name='detail_product'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/add-review/', views.AddReviewProduct.as_view(), name='add_review'),
    path('product/<int:pk>/update-review/', views.UpdateReviewProduct.as_view(), name='update_review'),
    path('product/<int:pk>/delete-review/', views.DeleteReviewProduct.as_view(), name='delete_review'),
]
