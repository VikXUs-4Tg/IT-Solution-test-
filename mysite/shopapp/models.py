from django.db import models

class Quote(models.Model):
    text = models.TextField(unique=True)  # Уникальное поле для предотвращения дубликатов
    source = models.ForeignKey('Source', on_delete=models.CASCADE) # Источник
    weight = models.IntegerField(default=1)  # Вес цитаты
    impressions = models.IntegerField(default=0)  # Количество показов
    likes = models.IntegerField(default=0)  # Количество лайков
    dislikes = models.IntegerField(default=0)  # Количество дизлайков

    def __str__(self):
        return self.text

class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name