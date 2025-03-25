from django.conf import settings
from django.db.models import Avg
from django.db import models
import uuid
import os
import json
from django.core.exceptions import ValidationError

def validate_step_image(image):
    if image and not image.name.lower().endswith(('.png', '.jpg', '.jpeg', ".pdf")):
        raise ValidationError('Неприпустимий формат зображення. Використовуйте .png, .jpg або .jpeg.')

def article_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('recipe_photos/main', unique_name)

def instruction_image_upload_to(instance, filename):
    # Зберігаємо зображення в media/instruction/<id рецепта>
    ext = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('instruction', str(instance.article.id), unique_name)




class Article(models.Model):
    title = models.CharField('Назва рецепту', max_length=100)
    photo = models.ImageField('Фотографія рецепту', upload_to=article_image_upload_to, null=True)
    description = models.TextField('Короткий опис')
    ingredients = models.TextField('Інгредієнти')
    notes = models.TextField('Примітки',  null=True)
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/recipes/{self.id}'

    # def average_rating(self):
    #     rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
    #     return round(rating, 1) if rating else '0'

    # def clean(self):
    #     super().clean()  # Викликаємо стандартний метод `clean`
    #
    #     # Перевірка, що поле instructions — це список
    #     if not isinstance(self.instructions, list):
    #         raise ValidationError('Інструкції мають бути списком.')
    #
    #     # Додаткова перевірка для кожного кроку
    #     for step in self.instructions:
    #         if 'text' not in step or not step['text']:
    #             raise ValidationError('Кожен крок повинен мати опис.')




class InstructionText(models.Model):
    article = models.ForeignKey(Article, related_name='instructions_text', on_delete=models.CASCADE)
    text = models.TextField('Текст інструкції')
    step_number = models.PositiveIntegerField('Номер кроку')  # Додаємо поле

    def __str__(self):
        return f"Instruction for {self.article.title} - Step {self.step_number}"



class InstructionImage(models.Model):
    article = models.ForeignKey(Article, related_name='instructions_image', on_delete=models.CASCADE)
    image = models.ImageField('Зображення інструкції', upload_to=instruction_image_upload_to)
    step_number = models.PositiveIntegerField('Номер кроку')  # Додаємо поле

    def __str__(self):
        return f"Image for {self.article.title} - Step {self.step_number}"

# def step_image_upload_to(instance, filename):
#     ext = filename.split('.')[-1]
#     unique_name = f"{uuid.uuid4().hex}.{ext}"
#     return os.path.join(f'steps/{instance.article.id}/', unique_name)


# class Step(models.Model):
#     article = models.ForeignKey(Article, related_name='steps', on_delete=models.CASCADE)
#     text = models.TextField('Опис кроку')
#     image = models.ImageField('Зображення кроку', upload_to=step_image_upload_to, blank=True, null=True)
#
#     def clean(self):
#         if self.image:
#             validate_step_image(self.image)
#
#     def __str__(self):
#         return f"Крок для: {self.article.title}"


# class Rating(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     article = models.ForeignKey(Article, related_name='ratings', on_delete=models.CASCADE)
#     rating = models.IntegerField(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)])
#
#     class Meta:
#         unique_together = ('user', 'article')
#
#     def __str__(self):
#         return f'{self.user.username} rated {self.article.title} {self.rating} stars'
