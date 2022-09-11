from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from ..models import Item, Order

User = get_user_model()


class ItemListViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        items = [
            Item(name=f'item {num}', price=10, stripe_product_id='qwerty', stripe_price_id='qwerty')
            for num in range(1, 4)
        ]
        Item.objects.bulk_create(items)

    def test_get(self):
        url = reverse('item_payment:items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('item_payment/items.html')
        self.assertEqual(len(response.context['items']), Item.objects.count())
        # items = Item.objects.all()
        # self.assertEqual(response.context['items'], items)


class ItemDetailViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        item = Item.objects.create(
            name='name',
            price=100,
            stripe_product_id='test',
            stripe_price_id='test',
        )

    def test_get(self):
        item = Item.objects.first()
        url = reverse('item_payment:item', kwargs={'pk': item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('item_payment/item.html')
        self.assertEqual(response.context_data['object'], item)
        self.assertEqual(response.context['item'], item)


class CreateCheckoutSessionViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        item = Item.objects.create(
            name='name',
            price=100,
            stripe_product_id='prod_MPbyKrmL1vJy4f',
            stripe_price_id='price_1LgmkNIV3zilNUERtP7HZsC7',
        )

    def test_post(self):
        item = Item.objects.first()
        url = reverse('item_payment:create_session', kwargs={'pk': item.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url[:34], 'https://checkout.stripe.com/c/pay/')


class AddItemToOrderViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        item = Item.objects.create(
            name='name',
            price=100,
            stripe_product_id='prod_MPbyKrmL1vJy4f',
            stripe_price_id='price_1LgmkNIV3zilNUERtP7HZsC7',
        )
        user = User.objects.create_user(username='user', password='123')

    def test_post(self):
        item = Item.objects.first()
        user = User.objects.first()
        url = reverse('item_payment:add_item_to_order', kwargs={'pk': item.pk})
        # none auth
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/add_item_to_order/{item.pk}/')
        # auth
        self.client.login(username='user', password='123')
        self.assertEqual(Order.objects.filter(user=user).first(), None)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/item/{item.pk}/')
        self.assertEqual(Order.objects.get(user=user).items.first(), item)


class MyOrderViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        items = [
            Item(name=f'item {num}', price=10, stripe_product_id='qwerty', stripe_price_id='qwerty')
            for num in range(1, 4)
        ]
        Item.objects.bulk_create(items)
        user = User.objects.create_user(username='test', password='123')
        order = Order.objects.create(user=user)
        order.items.add(*list(Item.objects.all()))

    def test_get(self):
        order = Order.objects.first()
        url = reverse('item_payment:my_order')
        # none auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/my_order/')
        # auth
        self.client.login(username='test', password='123')
        response = self.client.get(url)
        self.assertTemplateUsed('item_payment/my_order.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], order)


class EditItemOrderTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        items = [
            Item(name=f'item {num}', price=10, stripe_product_id='prod_MPbyKrmL1vJy4f', stripe_price_id='qwerty')
            for num in range(1, 4)
        ]
        Item.objects.bulk_create(items)
        user = User.objects.create_user(username='test', password='123')
        order = Order.objects.create(user=user)
        order.items.add(*list(Item.objects.all()))

    def test_get(self):
        order = Order.objects.first()
        item_in_order = order.items.first()
        self.assertEqual(order.items.count(), Item.objects.count())
        url = reverse('item_payment:edit_order', kwargs={'pk': item_in_order.pk})
        # none auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/edit_order/{item_in_order.pk}/')
        # auth
        self.client.login(username='test', password='123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('item_payment:my_order'))
        self.assertEqual(order.items.count(), 2)
        self.assertNotIn(Item.objects.get(pk=item_in_order.pk), order.items.all())


class CreateCheckoutSessionOrderViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        items = [
            Item(
                name=f'item {num}',
                price=10,
                stripe_product_id='qwerty',
                stripe_price_id='price_1LgmkNIV3zilNUERtP7HZsC7'
            )
            for num in range(1, 4)
        ]
        Item.objects.bulk_create(items)
        user = User.objects.create_user(username='test', password='123')
        order = Order.objects.create(user=user)
        order.items.add(*list(Item.objects.all()))

    def test_post(self):
        order = Order.objects.first()
        url = reverse('item_payment:pay_order', kwargs={'pk': order.pk})
        # none auth
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/login/?next=/pay_order/{order.pk}/')
        # auth
        self.client.login(username='test', password='123')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url[:34], 'https://checkout.stripe.com/c/pay/')


class RegisterViewTestCase(TestCase):

    def test_registration(self):
        data = {'username': 'test', 'password_1': '123', 'password_2': '123'}
        url = reverse('item_payment:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/register.html')

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


