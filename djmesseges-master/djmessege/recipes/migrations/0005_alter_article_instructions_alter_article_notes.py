# Generated by Django 5.1.3 on 2025-01-05 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_article_description_alter_article_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='instructions',
            field=models.JSONField(default=list, verbose_name='Інструкції'),
        ),
        migrations.AlterField(
            model_name='article',
            name='notes',
            field=models.TextField(default=1, verbose_name='Примітки'),
            preserve_default=False,
        ),
    ]
