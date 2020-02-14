from django.db import models

# Create your models here.
from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
CATEGORIES = (
            ("Depression", "Depression"),
            ("ADHD", "ADHD"),
            ("Autism", "Autism"),
            ("Anxiety", "Anxiety"),
            ("Bipolar", "Bipolar"),
            ("Eating Disorder", "Eating Disorder"),
            ('Anorexia', 'Anorexia'),
            ('Parenting','Parenting'),
            ('Children Behavior','Children Behavior'),
            ("Others", "Others"),
        )

class Blog(models.Model):

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.CharField(max_length=100, unique=False)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.CharField(max_length=100,choices = CATEGORIES, default="Others")
    status = models.IntegerField(choices=STATUS, default=0)
    img = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)

    def __unicode__(self):
        return '%s' % self.title

