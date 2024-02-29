from django.urls import include, path
from rest_framework import routers

from .views import ProductModelViewSet, LessonModelViewSet, ProductLessonsView

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'lessons', LessonModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/lessons/', ProductLessonsView.as_view()),
    ]
