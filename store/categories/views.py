# from django.shortcuts import render
# from rest_framework.views import APIView
# # Create your views here.
# from django.shortcuts import render
#
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from categories.models import Category
from categories.serializer import CategorySerializer
from categories.utils import get_parents, get_data_from_query_without_parent
from categories.validate.categories import CategoryValidate


class ArticleView(APIView):
    def post(self, request):
        validator = CategoryValidate()
        validator.validate(request.data)
        if validator.errors:
            return Response(validator.errors, status=HTTP_400_BAD_REQUEST)
        for category in validator.validated_data:
            Category.objects.create(name=category["name"], parent=category["parent"])
        return Response(status=HTTP_201_CREATED, data={"categories was successfully saved."})

    def get(self, request, pk):
        category = {}
        main_category = Category.objects.get(pk=pk)
        category["id"] = main_category.pk
        category["name"] = main_category.name
        category["parents"] = get_parents(main_category.parent)
        category["children"] = get_data_from_query_without_parent(Category.objects.filter(parent=main_category.name))
        category["siblings"] = get_data_from_query_without_parent(
            Category.objects.filter(parent=main_category.parent).exclude(name=main_category.name))
        return Response(status=HTTP_200_OK, data=category)
