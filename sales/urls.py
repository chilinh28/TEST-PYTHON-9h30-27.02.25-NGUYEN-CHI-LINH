from django.urls import path
from .views import upload_csv, get_sales

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('sales/', get_sales, name='get_sales'),
]
