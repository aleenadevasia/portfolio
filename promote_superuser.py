from django.contrib.auth.models import User

# Retrieve the user with id 12
user = User.objects.get(id=12)

# Set the user as a superuser
user.is_superuser = True
user.save()
