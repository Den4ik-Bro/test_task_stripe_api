import stripe
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, TemplateView
from .models import Item
from core import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    template_name = 'item_payment/item.html'


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        url = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': item.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url + '/success/',
            cancel_url=url + '/cancel/',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = 'item_payment/success.html'


class CancelView(TemplateView):
    template_name = 'item_payment/cancel.html'