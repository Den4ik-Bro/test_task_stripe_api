from django.urls import path
from . import views


app_name = 'item_payment'

urlpatterns = [
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item'),
    path('create_checkout_session/<int:pk>/', views.CreateCheckoutSessionView.as_view(), name='create_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='success'),
]