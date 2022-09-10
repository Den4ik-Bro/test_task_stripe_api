from django.urls import path
from . import views


app_name = 'item_payment'

urlpatterns = [
    path('items', views.ItemListView.as_view(), name='items'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item'),
    path('create_checkout_session/<int:pk>/', views.CreateCheckoutSessionView.as_view(), name='create_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='success'),
    path('order/<int:pk>/', views.CreateCheckoutSessionOrderView.as_view(), name='order')
]