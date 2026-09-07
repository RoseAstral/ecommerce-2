from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from .models import Store

# Create your tests here.
class StoreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.store = Store.objects.create(name="TestStore", owner="TestOwner")

    def test_store_creation(self):
        self.assertEqual(self.store.name, 'TestStore')
        self.assertEqual(self.store.owner, 'TestOwner')

    def test_string_representation(self):
        self.assertEqual(str(self.store.name), 'TestStore')

class HomepageViewTest(TestCase):
    def test_homepage_status_and_template(self):
        response = self.client.get(reverse('frontpage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/frontpage.html')
        self,self.assertContains(response, 'Ecommerce')