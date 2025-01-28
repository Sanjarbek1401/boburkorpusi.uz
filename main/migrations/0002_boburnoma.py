# Generated by Django 5.1.4 on 2025-01-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boburnoma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Sarlavha')),
                ('pdf_file', models.FileField(upload_to='boburnoma/', verbose_name='PDF fayl')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Yuklangan vaqt')),
            ],
            options={
                'verbose_name': 'Boburnoma',
                'verbose_name_plural': 'Boburnoma',
            },
        ),
    ]
