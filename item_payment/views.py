from django.shortcuts import render
from django.views.generic import DetailView
from .models import Item


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    template_name = 'item_payment/item.html'