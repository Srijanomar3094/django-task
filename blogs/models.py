from django.db import models
from user.models import Dropdown
from django.contrib.auth.models import User
from user.models import BaseModel

    

class Blog(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="blog_images/")
    category = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='user_blogs')
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True)
