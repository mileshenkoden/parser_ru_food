# Generated by Django 5.1.3 on 2025-01-05 10:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date',
        ),
        migrations.RemoveField(
            model_name='article',
            name='full_text',
        ),
        migrations.RemoveField(
            model_name='article',
            name='intro',
        ),
        migrations.AddField(
            model_name='article',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата створення'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.TextField(default='Опис відсутній', verbose_name='Короткий опис'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='ingredients',
            field=models.TextField(default='Опис відсутній', verbose_name='Інгредієнти'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='instructions',
            field=models.JSONField(default=list, verbose_name='Інструкції'),
        ),
        migrations.AddField(
            model_name='article',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Примітки'),
        ),
        migrations.AddField(
            model_name='article',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='recipe_photos/', verbose_name='Фотографія рецепту'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Назва рецепту'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recipes.article'),
        ),
    ]
