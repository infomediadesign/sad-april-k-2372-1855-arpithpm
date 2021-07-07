from django.test import TestCase
import requests
import json


class AnimalTestCase(TestCase):

    def test_check_pet_categories(self):
        """Animals that can speak are correctly identified"""
        a = requests.get("http://127.0.0.1:8000/api/petcategory/")
        self.assertEqual(a.status_code, 200)

    def test_check_length_of_pet_categories(self):
        """Animals that can speak are correctly identified"""
        a = requests.get("http://127.0.0.1:8000/api/petcategory/")
        a = json.loads(a.text)
        self.assertEqual(len(a), 2)

    def test_cat_exists_in_categories(self):
        """Animals that can speak are correctly identified"""
        a = requests.get("http://127.0.0.1:8000/api/petcategory/")
        self.assertIn("Cat", a.text)

    def test_payment_methods_len(self):
        a = requests.get("http://127.0.0.1:8000/api/paymentmethods/").json()
        self.assertEqual(len(a), 1)

    def test_payment_methods_exists(self):
        a = requests.get("http://127.0.0.1:8000/api/paymentmethods/").text
        self.assertIn("Cash On Delivery", a)
