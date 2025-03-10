from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from blogs.models import Blog
import json
from user.models import EmployeeDetail, Roles, Dropdown,LeftPanelRoute
from django.core.files.base import ContentFile
import base64
from django.shortcuts import get_object_or_404
from .models import Dropdown, Blog
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Appointment
import datetime
import googleapiclient.discovery
from django.utils import timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

def user_register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body.decode("utf-8"))
        elif request.content_type.startswith("multipart/form-data"):
            data = request.POST  
        else:
            return JsonResponse({"error": "Invalid Content-Type"}, status=400)

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password1", "").strip()
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()
        city = data.get("city", "").strip()
        state = data.get("state", "").strip()
        pincode = data.get("pincode", "").strip()
        role_id = data.get("role") 

       
        profile_picture_data = data.get("profile_picture") 
        profile_picture_file = request.FILES.get("profile_picture") 

      
        if not username or not email or not password or not first_name or not last_name or not address or not city or not state or not pincode:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if len(password) < 6:
            return JsonResponse({"error": "Password must be at least 6 characters long"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

       
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )

      
        employee_detail = EmployeeDetail.objects.create(
            user=user,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )

     
        if profile_picture_data:
            try:
                format, imgstr = profile_picture_data.split(";base64,")  
                ext = format.split("/")[-1]
                employee_detail.profile_picture.save(
                    f"profile_{user.id}.{ext}", 
                    ContentFile(base64.b64decode(imgstr)), 
                    save=True
                )
            except Exception as e:
                return JsonResponse({"error": f"Invalid profile picture format: {str(e)}"}, status=400)

        elif profile_picture_file:
            employee_detail.profile_picture = profile_picture_file
            employee_detail.save()

       
        if role_id:
            role_obj = Dropdown.objects.filter(id=role_id).first()
            if role_obj:
                Roles.objects.create(user=user, role=role_obj)
            else:
                return JsonResponse({"error": "Invalid role ID"}, status=400)

        return JsonResponse({"message": "User registered successfully"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)


def user_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)

        return JsonResponse({"error": "Invalid credentials"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)


def user_logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not logged in"}, status=400)

    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)


def user_roles(request):
    parent = Dropdown.objects.filter(field="User").first()
    categories = Dropdown.objects.filter(parent=parent.id).values('id','field')
    return JsonResponse(list(categories), safe=False)


def left_panel(request):
    user = request.user
    
    role = Roles.objects.filter(user=user).first()
    print("roles",role)
    user_role=role.role.field
    routes = LeftPanelRoute.objects.filter(role=role.role).distinct()

    routes_data = list(routes.values('name', 'path'))

    return JsonResponse({'routes': routes_data,'user_role':user_role}, safe=False)



def profile_data(request):
    user = request.user 
    user_role = Roles.objects.filter(user=user).first()
    
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "user_role": user_role.role.field if user_role and user_role.role else None,
        "employee_detail": {
            "profile_picture": user.employee_detail.profile_picture.url if user.employee_detail.profile_picture else None,
            "address": user.employee_detail.address,
            "city": user.employee_detail.city,
            "state": user.employee_detail.state,
            "pincode": user.employee_detail.pincode,
        }
    }
    return JsonResponse(data)




def get_blog_categories(request):
    parent = Dropdown.objects.filter(field="Blog Categories").first()
    categories = Dropdown.objects.filter(parent=parent.id).values("id", "field")
    return JsonResponse(list(categories), safe=False)

def create_blog(request):
    print("user",request.user)
    if request.method == "POST":
    
            title = request.POST.get("title")
            category_id = request.POST.get("category")
            summary = request.POST.get("summary")
            content = request.POST.get("content")
            is_draft = request.POST.get("is_draft", "false") == "true"
            image = request.FILES.get("image")

            category = get_object_or_404(Dropdown, id=category_id)

            blog = Blog.objects.create(
                title=title,
                image=image,
                category=category,
                summary=summary,
                content=content,
                is_draft=is_draft,
                author=request.user,
            )

            return JsonResponse({"message": "Blog created successfully", "blog_id": blog.id}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user.id).order_by("-created_at")
    
    blogs_data = [
        {
            "id": blog.id,
            "title": blog.title,
            "summary": blog.summary,
            "created_at": blog.created_at,
            "image": blog.image.url if blog.image and blog.image.name else None,
            "draft": blog.is_draft,
        }
        for blog in blogs
    ]
    
    return JsonResponse({"blogs": blogs_data})




def blog_list(request):
    blogs = Blog.objects.filter(is_draft=False).order_by("-created_at")
    data = {}

    for blog in blogs:
        category_name = blog.category.field if blog.category else "Uncategorized" 

        if category_name not in data:
            data[category_name] = []

        data[category_name].append({
            "id": blog.id,
            "title": blog.title,
            "summary": blog.summary,
            "created_at": blog.created_at,
            "image": blog.image.url if blog.image and blog.image.name else None,
        })

    return JsonResponse({"blogs": data})




def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, is_draft=False)
    blog_data = {
        "id": blog.id,
        "title": blog.title,
        "summary": blog.summary,
        "content": blog.content,
        "created_at": blog.created_at,
    }
    return JsonResponse(blog_data)





def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    return service



def get_doctors(request):
    if request.method == 'GET':
        doctor_role = Dropdown.objects.get(field='Doctor')
        doctors = User.objects.filter(user_roles__role=doctor_role)
        doctors_list = [{'id': doctor.id, 'name': doctor.first_name + ' ' + doctor.last_name, 'profile_picture': doctor.employee_detail.profile_picture.url} for doctor in doctors]
        return JsonResponse(doctors_list, safe=False)

def book_appointment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        doctor_id = data['doctor_id']
        speciality = data['speciality']
        date = data['date']
        start_time = data['start_time']
        
        start_datetime_naive = datetime.datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        start_datetime = timezone.make_aware(start_datetime_naive, timezone.get_current_timezone())
        end_datetime = start_datetime + datetime.timedelta(minutes=45)
        
        doctor = User.objects.get(id=doctor_id)
        patient = request.user
        
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            speciality=speciality,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
        
        service = get_calendar_service()
        event = {
            'summary': f'Appointment with {patient.first_name} {patient.last_name}',
            'description': f'Speciality: {speciality}',
            'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'UTC'},
        }
        calendar_event = service.events().insert(calendarId='srijanomar5840@gmail.com', body=event).execute()
        
        if 'id' in calendar_event:
            return JsonResponse({'message': 'Appointment booked successfully', 'event_id': calendar_event['id']})
        else:
            return JsonResponse({'message': 'Failed to book appointment'}, status=500)
        
def get_user_appointments(request):
    if request.method == 'GET':
        user = request.user
        appointments = Appointment.objects.filter(patient=user).select_related('doctor').order_by('-created_at')
        appointments_list = [
            {
                'doctor_name': appointment.doctor.first_name + ' ' + appointment.doctor.last_name,
                'appointment_date': appointment.start_datetime.date(),
                'start_time': appointment.start_datetime.time(),
                'end_time': appointment.end_datetime.time()
            } for appointment in appointments
        ]
        return JsonResponse(appointments_list, safe=False)
    
    