# Generated by Django 5.1.5 on 2025-02-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_dictionary_main_dictio_word_9b1b2c_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Muammo nomi')),
                ('content', models.TextField(verbose_name='Muammo matni')),
                ('order', models.IntegerField(default=0, verbose_name='Tartib raqami')),
            ],
            options={
                'verbose_name': 'Muammo',
                'verbose_name_plural': 'Muammolar',
                'ordering': ['order'],
            },
        ),
        migrations.DeleteModel(
            name='AdminContact',
        ),
    ]
