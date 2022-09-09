from django.urls import path
from . import views


app_name = 'item_payment'

urlpatterns = [
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item'),
]