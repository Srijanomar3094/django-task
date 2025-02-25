from django.contrib.auth.models import User
from django.db import models

class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = DeletedManager()
    
    class Meta:
        abstract = True

class Dropdown(models.Model):
    field = models.CharField(max_length=100)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='children')
    status=models.BooleanField(default=False, null=True, blank=True)
    order = models.IntegerField(default=0)
    objects = DeletedManager()
    def __str__(self):
        return self.field


class EmployeeDetail(BaseModel):
    user = models.OneToOneField(User, 
        on_delete=models.DO_NOTHING,
        related_name="employee_detail"
    )
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
  
class Roles(BaseModel):
    role = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='roles')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_roles')
    
    
class LeftPanelRoute(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    role = models.ForeignKey(Dropdown, related_name='left_panel_roles',on_delete=models.DO_NOTHING,null=True)
