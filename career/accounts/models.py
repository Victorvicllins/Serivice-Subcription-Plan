import uuid
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
def autoKey():
	sample = uuid.uuid4()
	key = hex(int(sample.time_low))[1:]
	return key

def upload_path(instance, filename):
	tx = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), tx)
	#return "images/%s/%s" % (instance.id, filename)
	return 'images/users/{0}/{1}'.format(instance.id, filename)

def upload_file_path(instance, filename):
	new_filename = random.randint(1,3910209312)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "files/{new_filename}/{final_filename}".format(
			new_filename=new_filename, 
			final_filename=final_filename
			)

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password(password) # change user password
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, password=None):
		user = self.create_user(
				email,
				password=password,
				is_staff=True
		)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(
				email,
				password=password,
				is_staff=True,
				is_admin=True
		)
		return user

class User(AbstractBaseUser):
	email       = models.EmailField(max_length=255, unique=True)
	name 		= models.CharField(max_length=255)
	active      = models.BooleanField(default=True) # can login 
	trainer     = models.BooleanField(default=False) # staff user non superuser
	admin       = models.BooleanField(default=False) # superuser 
	timestamp   = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email' #username
	# USERNAME_FIELD and password are required by default
	REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser

	objects = UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		if self.is_admin:
			return True
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

class UserProfile(models.Model):
	user 		 = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
	full_name    = models.CharField(max_length=255, blank=True, null=True)
	gender 		 = models.CharField(max_length=10)
	country 	 = models.CharField(max_length=255)
	phone 		 = models.CharField(max_length=255)
	avatar		 = models.ImageField(upload_to=upload_path, default='default.png', null=True, blank=True)
	city	 	 = models.CharField(max_length=150)
	
	def __str__(self):
		return f'{self.user.email}'

	#def get_absolute_url(self):
	#	return reverse('employee:staff_detail', kwargs={'id': self.id, 'staff_key': self.staff_key})

	def save(self, **kwargs):
		super().save()

		img = Image.open(self.avatar.path)
		if img.height > 350 or img.width > 350:
			output_size = (350, 350)
			img.thumbnail(output_size)

class TrainerProfile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trainer_profile')
    full_name       = models.CharField(max_length=255, help_text="Full Name..")
    address         = models.CharField(max_length=255, blank=True)
    vision          = models.CharField(max_length=255, help_text="Vision..")
    files           = models.FileField(upload_to=upload_file_path, null=True, blank=True)
    country         = models.CharField(max_length=200, default='Nigeria.')
    state           = models.CharField(max_length=120) # choices=ADDRESS_TYPES)
    city            = models.CharField(max_length=120)
    phone 	        = models.CharField(max_length=120)
    trainer_key 	= models.CharField(max_length = 100, default=autoKey())
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' %(self.user.name)

    #def get_absolute_url(self):
    #    return reverse("address-update", kwargs={"pk": self.pk})

    def get_company_email(self):
        return self.company_email

    def get_address(self):
        return "{for_name}\n{line1}\n{city}\n{state}, {phone}\n{country}".format(
                for_name = self.full_name or "",
                line1 = self.address,
                city = self.city,
                state = self.state,
                phone= self.phone,
                country = self.country
            )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.trainer:
		TrainerProfile.objects.get_or_create(user = instance)
	else:
		UserProfile.objects.get_or_create(user = instance)
	
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('_-----')
	# print(instance.internprofile.bio, instance.internprofile.location) 
	if instance.trainer:
		instance.trainer_profile.save()
	else:
		UserProfile.objects.get_or_create(user = instance)
