# Generated by Django 3.0.2 on 2020-02-11 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('bio', models.TextField(blank=True, max_length=5000)),
                ('address', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('concerns', models.CharField(blank=True, choices=[('Depression', 'Depression'), ('ADHD', 'ADHD'), ('Autism', 'Autism'), ('Anxiety', 'Anxiety'), ('Bipolar', 'Bipolar'), ('Behavior', 'Behavior'), ('Eating Disorder', 'Eating Disorder'), ('Others', 'Others')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
