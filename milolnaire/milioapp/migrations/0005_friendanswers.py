# Generated by Django 4.2.14 on 2024-07-29 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milioapp', '0004_questions_question_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('answer_type', models.CharField(choices=[('certain', 'Certain'), ('not_sure', 'Not sure'), ('dont_know', 'IDK')], default='certain', max_length=100)),
            ],
        ),
    ]
