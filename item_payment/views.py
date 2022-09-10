import stripe
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView, UpdateView, FormView
from stripe.error import InvalidRequestError
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationUserForm
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


class AddItemToOrderView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs['pk'])
        order, created = Order.objects.get_or_create(user=request.user)
        order.items.add(item)
        return redirect(reverse('item_payment:item', kwargs={'pk': item.pk}))


class MyOrderView(LoginRequiredMixin, DetailView):
    queryset = Order.objects.all()
    template_name = 'item_payment/my_order.html'
    context_object_name = 'order'

    def get(self, request, pk=None, *args, **kwargs):
        return super().get(request, pk)

    def get_object(self, queryset=None):
        order, _ = Order.objects.get_or_create(user=self.request.user)
        return order

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EditItemOrder(LoginRequiredMixin, UpdateView):
    model = Item

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        order = Order.objects.get(user=request.user)
        order.items.remove(item)
        return redirect(reverse('item_payment:my_order'))


class CreateCheckoutSessionOrderView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        line_items = []
        for item in order.items.all():
            price = {'price': item.stripe_price_id, 'quantity': item.count}
            line_items.append(price)

        url = 'http://127.0.0.1:8000'
        try:
            session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=url + '/success/',
                cancel_url=url + '/cancel/',
            )
        except InvalidRequestError:
            return redirect(reverse('item_payment:my_order'))
        return redirect(session.url)


class SuccessView(TemplateView):
    template_name = 'item_payment/success.html'


class CancelView(TemplateView):
    template_name = 'item_payment/cancel.html'


class RegistrationFormView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationUserForm

    def post(self, request, *args, **kwargs):
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            login_user = authenticate(request, username=user.username, password=form.cleaned_data['password_1'])
            login(request, login_user)
            return redirect(reverse('item_payment:items'))
        return render(request, self.template_name, context={'form': form})

