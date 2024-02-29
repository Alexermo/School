from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from products.models import Product, Lesson
from products.serializers import ProductSerializer, LessonSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(ProductModelViewSet, self).get_permissions()


# Create your views here.


class LessonModelViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(LessonModelViewSet, self).get_permissions()


class ProductLessonsView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, product_id, **kwargs):
        try:
            product = Product.objects.get(id=product_id)

            if request.user in product.users.all():

                lessons = Lesson.objects.filter(product=product)

                serializer = LessonSerializer(lessons, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "У вас нет доступных продуктов"},
                                status=status.HTTP_403_FORBIDDEN)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
