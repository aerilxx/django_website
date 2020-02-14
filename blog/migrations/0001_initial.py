# Generated by Django 3.0.2 on 2020-02-13 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('author', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('posted', models.DateField(auto_now_add=True, db_index=True)),
                ('category', models.CharField(choices=[('Depression', 'Depression'), ('ADHD', 'ADHD'), ('Autism', 'Autism'), ('Anxiety', 'Anxiety'), ('Bipolar', 'Bipolar'), ('Eating Disorder', 'Eating Disorder'), ('Anorexia', 'Anorexia'), ('Parenting', 'Parenting'), ('Children Behavior', 'Children Behavior'), ('Others', 'Others')], default='Others', max_length=100)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
                ('img', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
