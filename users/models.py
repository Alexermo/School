from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from products.models import Product
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    @classmethod
    def balance_groups(cls):
        all_groups = list(cls.objects.all())
        all_groups.sort(key=lambda group: group.students.count())

        while True:
            min_group = all_groups[0]
            max_group = all_groups[-1]

            if min_group.students.count() < max_group.students.count() - 1:
                student_to_move = max_group.students.order_by('id').last()
                max_group.students.remove(student_to_move)
                max_group.students.remove(student_to_move)
                min_group.students.add(student_to_move)
                all_groups.sort(key=lambda group: group.students.count())
            else:
                break

    @classmethod
    def assign_user(cls, user, product):
        # Если продукт уже начался, выйти из функции.
        if product.start_datetime <= timezone.now():
            return

        all_groups = list(cls.objects.filter(product=product))

        try:
            min_group = min(all_groups, key=lambda group: group.students.count())
            if min_group.students.count() < product.max_group_size:
                min_group.students.add(user)
                return min_group
            else:
                raise Exception('Группы заполнены')
        except Exception as e:
            print("Произошла ошибка:", e)

    @receiver(m2m_changed, sender=Product.users.through)
    def assign_user_to_group(sender, instance, action, pk_set, **kwargs):
        if action == "post_add":
            for user_id in pk_set:
                user = get_user_model().objects.get(pk=user_id)

                if user:
                    Group.assign_user(user, instance)
                else:
                    print(f"Пользователь с ID {user_id} не найден.")