import os
import django
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

# Import models after Django setup
from students.models import StudentProfile, Course, Enrollment, Grade, Attendance, Notification

def create_sample_data():
    """Create sample data for the student management system"""
    print("Creating sample data...")
    
    # Create a test user if it doesn't exist
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpassword123'
    
    try:
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )
        print(f"Created user: {username}")
    
    # Create a student profile if it doesn't exist
    try:
        student = StudentProfile.objects.get(user=user)
        print(f"Student profile for '{username}' already exists.")
    except StudentProfile.DoesNotExist:
        student = StudentProfile.objects.create(
            user=user,
            student_id='S12345',
            date_of_birth=datetime.date(2000, 1, 1)
        )
        student.address = '123 Test Street, Test City'
        student.phone_number = '123-456-7890'
        student.save()
        print(f"Created student profile for: {username}")
    
    # Create sample courses
    courses_data = [
        {
            'code': 'CS101',
            'name': 'Introduction to Computer Science',
            'description': 'An introductory course to computer science and programming.',
            'credits': 3,
            'instructor': 'Dr. John Smith',
            'start_date': datetime.date(2023, 9, 1),
            'end_date': datetime.date(2023, 12, 15),
        },
        {
            'code': 'MATH201',
            'name': 'Calculus I',
            'description': 'Introduction to differential and integral calculus.',
            'credits': 4,
            'instructor': 'Dr. Jane Doe',
            'start_date': datetime.date(2023, 9, 1),
            'end_date': datetime.date(2023, 12, 15),
        },
        {
            'code': 'ENG102',
            'name': 'English Composition',
            'description': 'A course focused on developing writing skills.',
            'credits': 3,
            'instructor': 'Prof. Robert Johnson',
            'start_date': datetime.date(2023, 9, 1),
            'end_date': datetime.date(2023, 12, 15),
        },
    ]
    
    created_courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            code=course_data['code'],
            defaults=course_data
        )
        created_courses.append(course)
        if created:
            print(f"Created course: {course.code} - {course.name}")
        else:
            print(f"Course '{course.code}' already exists.")
    
    # Create enrollments
    enrollments = []
    for course in created_courses:
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course,
            defaults={
                'enrollment_date': datetime.date(2023, 8, 15),
                'status': 'enrolled'
            }
        )
        enrollments.append(enrollment)
        if created:
            print(f"Enrolled {student.user.username} in {course.code}")
        else:
            print(f"{student.user.username} is already enrolled in {course.code}")
    
    # Create attendance records
    attendance_statuses = ['present', 'absent', 'late', 'excused']
    
    # Generate attendance for the past 30 days (excluding weekends)
    for enrollment in enrollments:
        # Get the course start date
        start_date = max(enrollment.course.start_date, timezone.now().date() - datetime.timedelta(days=30))
        end_date = min(enrollment.course.end_date, timezone.now().date())
        
        current_date = start_date
        while current_date <= end_date:
            # Skip weekends (Saturday=5, Sunday=6)
            if current_date.weekday() < 5:
                # Randomly select a status with higher probability for 'present'
                import random
                weights = [0.8, 0.05, 0.1, 0.05]  # 80% present, 5% absent, 10% late, 5% excused
                status = random.choices(attendance_statuses, weights=weights, k=1)[0]
                
                attendance, created = Attendance.objects.get_or_create(
                    enrollment=enrollment,
                    date=current_date,
                    defaults={
                        'status': status,
                    }
                )
                
                if created:
                    if status == 'absent':
                        attendance.remarks = 'Student was absent'
                    elif status == 'late':
                        attendance.remarks = 'Student arrived 15 minutes late'
                    elif status == 'excused':
                        attendance.remarks = 'Excused due to medical appointment'
                    attendance.save()
                    
                    print(f"Created attendance record for {enrollment.student.user.username} in {enrollment.course.code} on {current_date}: {status}")
            
            current_date += datetime.timedelta(days=1)
    
    # Create a notification
    Notification.objects.create(
        user=user,
        title='Welcome to the Student Management System',
        message='Thank you for joining our platform. Start exploring your courses and track your progress!',
        is_read=False
    )
    print(f"Created welcome notification for {username}")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data() 