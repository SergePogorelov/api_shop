from rest_framework.test import APITestCase as TestCase
from rest_framework.test import APIClient as Client

from shop.models import Category, Product


class TestCategories(TestCase):

    def setUp(self):
        self.client = Client()

    def test_creating_categories(self):
        response = self.client.post("/api/categories/")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/api/categories/", {"name": "new_category_1"}
        )
        self.assertEqual(response.status_code, 201)

        category = Category.objects.all().count()
        self.assertEqual(category, 1)

    def test_deleting_categories(self):
        self.client.post("/api/categories/", {"name": "new_category_1"})

        response = self.client.delete("/api/categories/1/")
        self.assertEqual(response.status_code, 204)

        category = Category.objects.all().count()
        self.assertEqual(category, 0)

        response = self.client.delete("/api/categories/1/")
        self.assertEqual(response.status_code, 404)

    def test_unresolved_methods(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 405)

        response = self.client.get("/api/categories/1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.put("/api/categories/1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.patch("/api/categories/1/")
        self.assertEqual(response.status_code, 405)


class TestProduct(TestCase):

    def setUp(self):
        self.client = Client()
        for i in range(1, 12):
            self.client.post("/api/categories/", {"name": f"new_category_{i}"})

    def creat_product(self, categories=None):
        data = {"name": "new_product", "price": 200}

        if categories:
            data["categories"] = categories

        return self.client.post("/api/products/", data)

    def test_creating_product(self):
        response = self.client.post("/api/products/")
        self.assertEqual(response.status_code, 400)

        response = self.creat_product()
        self.assertEqual(response.status_code, 400)

        response = self.creat_product([1])
        self.assertEqual(response.status_code, 400)

        response = self.creat_product(list(range(1, 12)))
        self.assertEqual(response.status_code, 400)

        response = self.creat_product([1, 2])
        self.assertEqual(response.status_code, 201)

        product = Product.objects.all().count()
        self.assertEqual(product, 1)

    def test_delete_product(self):
        self.creat_product([1, 2])
        product = Product.objects.get(pk=1)
        self.assertEqual(product.deleted, False)

        response = self.client.delete(f"/api/products/{product.id}/")
        product = Product.objects.get(pk=1)
        self.assertEqual(product.deleted, True)
        self.assertEqual(Product.objects.all().count(), 1)


class TestCategoryProduct(TestCase):

    def setUp(self):
        self.client = Client()

        for i in range(1, 3):
            self.client.post("/api/categories/", {"name": f"new_category_{i}"})
        
        data = {
            "name": "new_product",
            "price": 200,
            "categories": list(range(1, 3)),
        }
        self.client.post("/api/products/", data)

    def test_fail_delete_category(self):
        category = Category.objects.get(pk=1)
        self.assertEqual(category.products.all().count(), 1)

        response = self.client.delete(f"/api/categories/{category.pk}/")
        self.assertEqual(response.status_code, 400)

        self.assertEqual(category.products.all().count(), 1)


class TestProductsFilters(TestCase):

    def setUp(self):
        self.client = Client()

        for i in range(1, 13):
            self.client.post("/api/categories/", {"name": f"new_category_{i}"})
        
        for i in range(1, 12):

            data = {
                "name": f"new_product_{i}",
                "price": 10*i,
                "categories": [i, i+1],
            }
            self.client.post("/api/products/", data)

        self.client.post(
            "/api/products/", 
            {
                "name":"unpublished", 
                "price": 100, 
                "categories": [1,2], 
                "published": False
            }
        )

    def test_name_filter(self):
        response = self.client.get("/api/products/", {"name":"new_product_1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("new_product_1", response.content.decode("utf-8"))
        self.assertNotIn("new_product_2", response.content.decode("utf-8"))
        
    def test_category_filter(self):
        response = self.client.get("/api/products/", {"categories":"new_category_1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("new_category_1", response.content.decode("utf-8"))
        self.assertNotIn("new_category_3", response.content.decode("utf-8"))
        
    def test_price_filter(self):
        response = self.client.get("/api/products/", {"price_from":10, "price_to": 30})
        self.assertEqual(response.status_code, 200)
        self.assertIn('"price":"10.00"', response.content.decode("utf-8"))
        self.assertIn('"price":"20.00"', response.content.decode("utf-8"))
        self.assertIn('"price":"30.00"', response.content.decode("utf-8"))
        self.assertNotIn('"price":"40.00"', response.content.decode("utf-8"))
    
    def test_published_filter(self):
        response = self.client.get("/api/products/", {"published": True})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('"published":false', response.content.decode("utf-8"))
        self.assertIn('"published":true', response.content.decode("utf-8"))
        
        response = self.client.get("/api/products/", {"published": False})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('"published":true', response.content.decode("utf-8"))
        self.assertIn('"published":false', response.content.decode("utf-8"))
        