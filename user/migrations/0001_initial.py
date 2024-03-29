# Generated by Django 3.0.2 on 2020-03-02 22:22

from django.conf import settings
import django.core.validators
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
                ('avatar', models.ImageField(blank=True, null=True, upload_to='uploads/avatar')),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('bio', models.TextField(blank=True, max_length=5000)),
                ('address', models.CharField(blank=True, max_length=30)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Non Binary', 'Non Binary')], default='none', max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('concerns', models.CharField(blank=True, choices=[('Depression', 'Depression'), ('ADHD', 'ADHD'), ('Autism', 'Autism'), ('Anxiety', 'Anxiety'), ('Bipolar', 'Bipolar'), ('Behavior', 'Behavior'), ('Eating Disorder', 'Eating Disorder'), ('Others', 'Others')], max_length=50)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('body', models.TextField()),
                ('posted_at', models.DateField(auto_now_add=True, db_index=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.IntegerField()),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, choices=[('09:00:00', '09 AM'), ('10:00:00', '10 AM'), ('11:00:00', '11 AM'), ('13:00:00', '01 PM'), ('14:00:00', '02 PM'), ('15:00:00', '03 PM'), ('16:00:00', '04 PM')], null=True)),
                ('note', models.TextField(blank=True, max_length=5000)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile')),
            ],
            options={
                'ordering': ('date',),
            },
        ),
    ]
