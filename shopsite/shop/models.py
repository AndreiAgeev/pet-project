from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()


class Category(models.Model):
    """
    Модель, описывающая категории товаров.

    Содержит название категории и её слаг. Слаг использается в URL.
    """

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Индентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL;'
        ' разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    def __str__(self) -> str:
        """Делаем так, чтобы в админ-панеле отображались названия категорий."""
        return self.name

    class Meta:
        """Настройки для админ-панели для категорий."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """
    Модель, описывающая товары.

    Содержит название товара, его цену, описание, категорию и среднюю оценку,
    высчитываемую на основе отзывов
    """

    name = models.CharField('Название', max_length=256)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание товара')
    avg_score = models.FloatField(
        'Средняя оценка',
        null=True,
        blank=False,
        validators=(
            MaxValueValidator(limit_value=5),
            MinValueValidator(limit_value=0)
        ),
    )
    Category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория',
        related_name='products'
    )

    # Описать данную функцию потом, после создания view и urlpatterns
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        """Делаем так, чтобы в админ-панеле отображались названия товаров."""
        return self.name

    class Meta:
        """Настройки для админ-панели для товаров."""

        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        ordering = ('avg_score',)


class Review(models.Model):
    """
    Модель, описывающая отзывы на товары.

    Содержит текст отзыва, оценку товара от 0 до 5 и дату публикации отзыва.
    Также связана с моделями User и Product через Foreign Key.
    """

    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MaxValueValidator(limit_value=5)]
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='reviews',

    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        """Настройки для админ-панели для отзывов."""

        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('created_at',)
