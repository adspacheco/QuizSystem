# Generated by Django 3.0.1 on 2020-01-04 20:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0016_auto_20200103_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradedquiz',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='homework.Question'),
        ),
        migrations.AlterField(
            model_name='gradedquiz',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.Quiz'),
        ),
    ]
