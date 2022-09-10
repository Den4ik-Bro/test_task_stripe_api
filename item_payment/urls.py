from django.urls import path
from . import views


app_name = 'item_payment'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='items'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item'),
    path('create_checkout_session/<int:pk>/', views.CreateCheckoutSessionView.as_view(), name='create_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='success'),
    path('add_item_to_order/<int:pk>/', views.AddItemToOrderView.as_view(), name='add_item_to_order'),
    path('my_order/', views.MyOrderView.as_view(), name='my_order'),
    path('pay_order/<int:pk>/', views.CreateCheckoutSessionOrderView.as_view(), name='pay_order'),
    path('edit_order/<int:pk>/', views.EditItemOrder.as_view(), name='edit_order'),
    path('register/', views.RegistrationFormView.as_view(), name='register'),
]