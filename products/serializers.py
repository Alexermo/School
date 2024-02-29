from rest_framework import fields, serializers

from products.models import Product, Lesson
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'lessons', 'start_datetime')

    def create(self, validated_data):
        creator_id = self.context['request'].user.id
        return Product.objects.create(creator_id=creator_id, **validated_data)

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return LessonSerializer(lessons, many=True).data


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('title', 'description')
