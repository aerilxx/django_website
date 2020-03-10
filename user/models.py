from __future__ import unicode_literals
 
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
# encrypt note model
import cryptography
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class Profile(models.Model):
	CHOICES = (
	    ("Depression", "Depression"),
	    ("ADHD", "ADHD"),
	    ("Autism", "Autism"),
	    ("Anxiety", "Anxiety"),
	    ("Bipolar", "Bipolar"),
	    ("Behavior", "Behavior"),
	    ("Eating Disorder", "Eating Disorder"),
	    ("Others", "Others"),
	)
	USER_GENDER = (
		('Male', 'Male'), 
		('Female', 'Female'),
		('Non Binary', 'Non Binary'),
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='uploads/avatar', null=True, blank=True)

	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
	    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
	bio = models.TextField(max_length=5000, blank=True)
	address = models.CharField(max_length=30,  blank=True)
	gender = models.CharField(max_length=10, choices=USER_GENDER, default='none')
	birth_date = models.DateField(blank=True, null=True)
	email_confirmed = models.BooleanField(default=False)
	concerns = models.CharField(max_length = 50, choices = CHOICES, blank=True)
	created_at = models.DateField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return self.user.username

	def get_avatar(self):
		if not self.avatar:
			return '/static/img/avater.jpeg'
		return self.avatar.url

	def avatar_tag(self):
		return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())
 
# functions related to forum post
	def get_total_posts(self):
		return self.post_set.count()

	def get_total_replies(self):
		return self.comment_set.count()


def generate_key(password):
	p = password.encode() 
	salt = b'aeril_'
	kdf = PBKDF2HMAC(
	    algorithm=hashes.SHA256(),
	    length=32,
	    salt=salt,
	    iterations=100000,
	    backend=default_backend()
	)
	key = base64.urlsafe_b64encode(kdf.derive(p))
	return key


class Notebook(models.Model):
	created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	# encrypt context for privacy protection 
	body = models.TextField(null=False, blank=False)
	body_store =  models.BinaryField(default=b'')
	posted_at = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title

	def decrypt_context(self, key):
		msg = self.body_store
		f = Fernet(key)
		decrypted = f.decrypt(msg)

		return decrypted

	def save(self,*args, **kwargs):
		key = generate_key(self.created_by.user.password)
		message = self.body.encode()
		f = Fernet(key)
		self.body="we delete note body after stored it in binary form"
		self.body_store = f.encrypt(message)
		super(Notebook, self).save(*args, **kwargs)


          
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
