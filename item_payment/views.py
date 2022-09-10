import stripe
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView
from .models import Item, Order
from core import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    template_name = 'item_payment/item.html'


class ItemListView(ListView):
    queryset = Item.objects.all()
    template_name = 'item_payment/items.html'
    context_object_name = 'items'


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs['pk'])
        url = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': item.stripe_price_id,
                    'quantity': item.count,
                },
            ],
            mode='payment',
            success_url=url + '/success/',
            cancel_url=url + '/cancel/',
        )
        return redirect(checkout_session.url)


class CreateCheckoutSessionOrderView(View):

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        line_items = []
        for item in order.items.all():
            price = {'price': item.stripe_price_id, 'quantity': item.count}
            line_items.append(price)

        url = 'http://127.0.0.1:8000'
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=url + '/success/',
            cancel_url=url + '/cancel/',
        )
        return redirect(session.url)


class SuccessView(TemplateView):
    template_name = 'item_payment/success.html'


class CancelView(TemplateView):
    template_name = 'item_payment/cancel.html'