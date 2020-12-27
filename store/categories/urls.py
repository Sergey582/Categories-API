from django.urls import path
from .views import ArticleView

app_name = "categories"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('categories/', ArticleView.as_view()),
    path('categories/<int:pk>/', ArticleView.as_view()),
]
