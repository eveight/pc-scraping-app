import jsonfield
from django.db import models


class Component(models.Model):
    component = models.CharField(max_length=120, unique=True, default='Комплектующая')

    class Meta:
        verbose_name = 'Комплектующая'
        verbose_name_plural = 'Комплектующие'

    def __str__(self):
        return self.component


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=120, unique=True, verbose_name='Название производителя')

    class Meta:
        verbose_name = 'Производитель видеокарты'
        verbose_name_plural = 'Производитель видеокарт'

    def __str__(self):
        return self.manufacturer_name


class Gpu(models.Model):
    img = models.URLField(verbose_name='Картинка')
    name = models.CharField(max_length=120, unique=True, verbose_name='Название')
    model = models.CharField(max_length=120, verbose_name='Модель')
    wed_price = models.CharField(max_length=120, verbose_name='Средняя цена')
    best_price = models.URLField(verbose_name='Лучшая цена')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель видеокарты',
                                     blank=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Комплектующая', blank=True)

    class Meta:
        verbose_name = 'Видеокарта'
        verbose_name_plural = 'Видеокарты'

    def __str__(self):
        res = str(self.name) + ' ' + str(self.model)
        return res


class Cpu(models.Model):
    img = models.URLField(verbose_name='Картинка')
    name = models.CharField(max_length=120, unique=True, verbose_name='Название')
    model = models.CharField(max_length=120, verbose_name='Модель')
    wed_price = models.CharField(max_length=120, verbose_name='Средняя цена')
    best_price = models.URLField(verbose_name='Лучшая цена')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель процессора',
                                     blank=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Комплектующая', blank=True)

    class Meta:
        verbose_name = 'Процессор'
        verbose_name_plural = 'Процессоры'

    def __str__(self):
        res = str(self.name) + ' ' + str(self.model)
        return res


class Url(models.Model):
    component_url = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Комплектующая')
    manufacturer = models.CharField(max_length=120, verbose_name='Производитель')
    model = models.CharField(max_length=120, verbose_name='Модель')
    url = models.URLField()

    class Meta:
        verbose_name = 'Url адресс'
        verbose_name_plural = 'Url адресса'

    def __str__(self):
        res = str(self.manufacturer) + ' ' + str(self.model)
        return res


class Errors(models.Model):
    time = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return str(self.time)
