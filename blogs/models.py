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
    
    
class Appointment(BaseModel):
    doctor = models.ForeignKey(User, related_name='doctor_appointments', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patient_appointments', on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.speciality} on {self.start_datetime}"


