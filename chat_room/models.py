from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your models here.

User = get_user_model()

class Group(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable= False)
    members = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, null=True, blank= True, on_delete=models.CASCADE, related_name="Author")
    name = models.CharField(max_length=50, null=True, blank= True)
    
    def save(self, *args, **kwargs):
        if not self.name:
            user = self.created_by
            base_name = slugify(user.username) + "_group_"
            existing_names = Group.objects.filter(name__startswith=base_name).values_list('name', flat=True)
            if existing_names:
                # Get the numerical suffix of the last group name and increment it
                last_suffix = max([int(name.split('_')[-1]) for name in existing_names])
                self.name = f"{base_name}{last_suffix + 1}"
            else:
                self.name = f"{base_name}1"
        super().save(*args, **kwargs)
    
    def add_user(self, user):
        self.members.add(user)
        self.save()
        return

    def remove_user(self, user):
        self.members.remove(user)
        self.save()
        return
    
    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add= True)
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete= models.CASCADE)

