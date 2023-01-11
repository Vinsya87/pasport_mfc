from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

WAITING = 'В обработке'
REVIEWS_NO = 'Отказано'
REVIEWS_YES = 'Выполнено'
ISSUED = 'Выдано'


class Service(models.Model):
    reviews = (
        (WAITING, WAITING),
        (REVIEWS_NO, REVIEWS_NO),
        (REVIEWS_YES, REVIEWS_YES),
        (ISSUED, ISSUED)
    )
    failure = models.TextField(
        'Причина отказа',
        blank=True,
        null=True,
        help_text='Введите причину отказа'
    )
    review = models.CharField(
        'Одобрение',
        choices=reviews,
        max_length=max(len(role[1]) for role in reviews), default=WAITING
    )
    fio_user = models.CharField(
      'Ваше ФИО',
      max_length=150, blank=False)
    fio_mother = models.CharField(
      'ФИО Матери',
      max_length=150, blank=False)
    fio_father = models.CharField(
      'ФИО Отца',
      max_length=150, blank=False)
    date_of_birth = models.DateTimeField(
        'Дата рождения',
    )
    serial = models.CharField('Серия паспорта', max_length=25)
    number = models.CharField('Номер паспорта', max_length=25)
    phone = models.CharField(
      verbose_name='Номер телефона для связи', max_length=20,
      unique=True, null=True, blank=False)
    image = models.ImageField(
        'Фото на паспорт',
        upload_to='services/',
        blank=False,
        help_text='Загрузите фото'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['-pub_date', '-pk']
        verbose_name = 'Замена паспорта'
        verbose_name_plural = 'Замена паспортов'

    def __str__(self):
        return 'Автор {} {}'.format(
          self.author.first_name, self.author.last_name)


class Extradition(models.Model):
    reviews = (
        (WAITING, WAITING),
        (REVIEWS_NO, REVIEWS_NO),
        (REVIEWS_YES, REVIEWS_YES),
        (ISSUED, ISSUED)
    )
    failure = models.TextField(
        'Причина отказа',
        blank=True,
        null=True,
        help_text='Введите причину отказа'
    )
    review = models.CharField(
        'Одобрение',
        choices=reviews,
        max_length=max(len(role[1]) for role in reviews), default=WAITING
    )
    fio_user = models.CharField(
        'Ваше ФИО',
        max_length=150, blank=False)
    fio_mother = models.CharField(
        'ФИО Матери',
        max_length=150, blank=False)
    fio_father = models.CharField(
        'ФИО Отца',
        max_length=150, blank=False)
    phone = models.CharField(
      verbose_name='Номер телефона для связи', max_length=20,
      unique=True, null=True, blank=False)
    birth_certificate = models.CharField(
        'Номер свидетельства о рождении',
        blank=False, max_length=25
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='extraditions',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Фото на паспорт',
        upload_to='services/',
        blank=False,
        null=True,
        help_text='Загрузите фото'
    )

    class Meta:
        ordering = ['-pub_date', '-pk']
        verbose_name = 'Выдача паспорта'
        verbose_name_plural = 'Выдача паспортов'

    def __str__(self):
        return 'Автор {} {}'.format(
          self.author.first_name, self.author.last_name)
