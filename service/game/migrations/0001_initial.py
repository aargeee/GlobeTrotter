# Generated by Django 5.1.6 on 2025-03-01 20:05

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DestinationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('CLUE', 'Clue'), ('FUN_FACT', 'Fun Fact'), ('TRIVIA', 'Trivia')], max_length=10)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.destination')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_answered_correctly', models.BooleanField(default=False)),
                ('clues', models.ManyToManyField(limit_choices_to={'type': 'CLUE'}, to='game.destinationinfo')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.destination')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
        migrations.AddIndex(
            model_name='destinationinfo',
            index=models.Index(fields=['destination', 'type'], name='game_destin_destina_4dbc50_idx'),
        ),
        migrations.AddIndex(
            model_name='game',
            index=models.Index(fields=['player', 'is_active'], name='game_game_player__cd5619_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['game', 'is_answered_correctly'], name='game_questi_game_id_d2881d_idx'),
        ),
    ]
