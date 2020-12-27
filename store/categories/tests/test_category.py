from django.test import TestCase

# Create your tests here.
from categories.models import Category
from categories.validate.categories import CategoryValidate


class ArticleViewTestCase(TestCase):
    def test_post(self):
        data = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {
                                    "name": "Category 1.1.1.1"
                                },
                                {
                                    "name": "Category 1.1.1.2"
                                },
                                {
                                    "name": "Category 1.1.1.3"
                                }
                            ]
                        },
                        {
                            "name": "Category 1.1.2",
                            "children": [
                                {
                                    "name": "Category 1.1.2.1"
                                },
                                {
                                    "name": "Category 1.1.2.2"
                                },
                                {
                                    "name": "Category 1.1.2.3"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Category 1.2",
                    "children": [
                        {
                            "name": "Category 1.2.1"
                        },
                        {
                            "name": "Category 1.2.2",
                            "children": [
                                {
                                    "name": "Category 1.2.2.1"
                                },
                                {
                                    "name": "Category 1.2.2.2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post('/api/categories/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"categories was successfully saved."})

        data = {"name": ["cat1"], }
        response = self.client.post('/api/categories/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, [{'value error': "name ['cat1'] must be string"}])

    def test_get(self):
        Category.objects.create(pk=1, name="cat1", parent=None)
        Category.objects.create(pk=2, name="cat1.1", parent="cat1")
        Category.objects.create(pk=3, name="cat1.2", parent="cat1")
        Category.objects.create(pk=4, name="cat1.1.1", parent="cat1.1")
        Category.objects.create(pk=5, name="cat1.1.1.1", parent="cat1.1.1")
        response = self.client.get('/api/categories/4/')

        right_response = {
            "id": 4,
            "name": "cat1.1.1",
            "children": [
                {
                    "id": 5,
                    "name": "cat1.1.1.1"
                }
            ],
            "parents": [
                {
                    "id": 2,
                    "name": "cat1.1"
                },
                {
                    "id": 1,
                    "name": "cat1"
                }

            ],
            "siblings": [

            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, right_response)

        response = self.client.get('/api/categories/2/')
        right_response_with_siblings = {
            "id": 2,
            "name": "cat1.1",
            "children": [
                {
                    "id": 4,
                    "name": "cat1.1.1"
                }
            ],
            "parents": [
                {
                    "id": 1,
                    "name": "cat1"
                }

            ],
            "siblings": [
                {
                    "id": 3,
                    "name": "cat1.2"
                }

            ]
        }
        self.assertEqual(response.data, right_response_with_siblings)

        response = self.client.get('/api/categories/1/')
        right_response_root = {
            "id": 1,
            "name": "cat1",
            "children": [
                {
                    "id": 2,
                    "name": "cat1.1"
                },
                {
                    "id": 3,
                    "name": "cat1.2"
                }
            ],
            "parents": [],
            "siblings": []
        }
        self.assertEqual(response.data, right_response_root)

        response = self.client.get('/api/categories/1121/')
        self.assertEqual(response.status_code, 404)
