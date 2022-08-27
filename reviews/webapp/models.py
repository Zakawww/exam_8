from django.contrib.auth.models import User
from django.db import models


CATEGORY_CHOICES = (
    ('other', 'Другое'),
    ('hardware', 'Компьютеры'),
    ('software', 'Программное обеспечение'),
    ('phones', 'Телефоны')
)

RATING_CHOICES = (
    (5, 'Отлично'),
    (4, 'Хорошо'),
    (3, 'Удовлентворительно'),
    (2, 'Плохо'),
    (1, 'Очень плохо')
)


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Товар')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0],
                                verbose_name='Категория')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='Картинка')

    def avg_rating(self):
        ratings = Review.objects.filter(product=self.pk)
        count = 0
        for rating in ratings:
            count += rating.rating
        try:
            avg = count / len(ratings)
            avg = round(avg, 1)
        except ZeroDivisionError:
            avg = 'Не оценивался'

        return avg

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey('webapp.Product', related_name='reviews', on_delete=models.CASCADE, verbose_name='Товар')
    description = models.TextField(max_length=3000, verbose_name='Текст отзыва')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
