from django.test import TestCase

# Create your tests here.
from categories.models import Category
from categories.validate.categories import CategoryValidate


class CategoryValidateTestCase(TestCase):

    def test_validate(self):
        validator = CategoryValidate()
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
        validator.validate(data)
        self.assertEqual(validator.errors, [])

        empty_data = {}
        validator = CategoryValidate()
        validator.validate(empty_data)
        self.assertEqual(validator.errors, [{'structure error': 'empty data'}])

        data_with_invalid_name = {"name": 12}
        validator = CategoryValidate()
        validator.validate(data_with_invalid_name)
        self.assertEqual(validator.errors, [{'value error': 'name 12 must be string'}])

        data_with_invalid_children = {"name": "Maks", "children": ""}
        validator = CategoryValidate()
        validator.validate(data_with_invalid_children)
        self.assertEqual(validator.errors, [{'structure error': "'children' input data must be list"}])

        data_with_empty_name = {"name": ""}
        validator = CategoryValidate()
        validator.validate(data_with_empty_name)
        self.assertEqual(validator.errors, [{'value error': 'name is required'}])

        data_with_invalid_format = []
        validator = CategoryValidate()
        validator.validate(data_with_invalid_format)
        self.assertEqual(validator.errors, [{'structure error': 'input data must be dict'}])

        data_with_duplicate_names = {"name": "cat1", "children": [{"name": "cat1"}]}
        validator = CategoryValidate()
        validator.validate(data_with_duplicate_names)
        self.assertEqual(validator.errors, [{'value error': 'cat1 must be unique'}])

        data_with_duplicate_names = {"name": "cat1"}
        Category.objects.create(name="cat1", parent=None)
        validator = CategoryValidate()
        validator.validate(data_with_duplicate_names)
        self.assertEqual(validator.errors, [{'value error': 'cat1 must be unique'}])
