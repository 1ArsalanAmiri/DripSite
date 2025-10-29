from django.test import TestCase , SimpleTestCase

# Create your tests here.
class TestProduct(TestCase):
    def test_product_status_code(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)