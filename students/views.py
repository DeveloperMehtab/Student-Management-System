from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone
from .models import StudentProfile, Course, Enrollment, Grade, Notification, Attendance
from .forms import UserRegisterForm, StudentProfileForm, UserUpdateForm, CourseEnrollForm

def home(request):
    """Home page view"""
    courses_count = Course.objects.count()
    students_count = StudentProfile.objects.count()
    
    context = {
        'title': 'Home',
        'courses_count': courses_count,
        'students_count': students_count,
    }
    
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """Dashboard view for logged-in students"""
    try:
        student = request.user.student_profile
        enrollments = Enrollment.objects.filter(student=student)
        
        # Get recent notifications
        notifications = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).order_by('-created_at')[:5]
        
        context = {
            'title': 'Dashboard',
            'student': student,
            'enrollments': enrollments,
            'notifications': notifications,
        }
        
        return render(request, 'students/dashboard.html', context)
    except StudentProfile.DoesNotExist:
        messages.warning(request, "Please complete your student profile first.")
        return redirect('students:edit_profile')

@login_required
def profile(request):
    """View student profile"""
    try:
        student = request.user.student_profile
        context = {
            'title': 'Profile',
            'student': student,
        }
        return render(request, 'students/profile.html', context)
    except StudentProfile.DoesNotExist:
        messages.warning(request, "Please complete your student profile first.")
        return redirect('students:edit_profile')

@login_required
def edit_profile(request):
    """Edit student profile"""
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        student = None
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = StudentProfileForm(
            request.POST, 
            request.FILES, 
            instance=student
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            
            if student is None:
                # Create new profile if it doesn't exist
                profile = profile_form.save(commit=False)
                profile.user = request.user
                profile.save()
            else:
                profile_form.save()
                
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('students:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = StudentProfileForm(instance=student)
    
    context = {
        'title': 'Edit Profile',
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'students/edit_profile.html', context)

@login_required
def course_list(request):
    """View list of all courses"""
    courses = Course.objects.all().order_by('code')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        courses = courses.filter(
            Q(code__icontains=query) | 
            Q(name__icontains=query) | 
            Q(instructor__icontains=query)
        )
    
    context = {
        'title': 'Courses',
        'courses': courses,
        'query': query,
    }
    
    return render(request, 'students/course_list.html', context)

@login_required
def course_detail(request, course_id):
    """View details of a specific course"""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if student is enrolled
    is_enrolled = False
    try:
        student = request.user.student_profile
        is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    except StudentProfile.DoesNotExist:
        pass
    
    context = {
        'title': course.name,
        'course': course,
        'is_enrolled': is_enrolled,
    }
    
    return render(request, 'students/course_detail.html', context)

@login_required
def enroll_course(request, course_id):
    """Enroll in a course"""
    course = get_object_or_404(Course, id=course_id)
    
    try:
        student = request.user.student_profile
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.warning(request, f"You are already enrolled in {course.name}.")
        else:
            # Create enrollment
            enrollment = Enrollment(
                student=student,
                course=course,
                enrollment_date=timezone.now().date()
            )
            enrollment.save()
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                title=f"Enrolled in {course.code}",
                message=f"You have successfully enrolled in {course.name}."
            )
            
            messages.success(request, f"Successfully enrolled in {course.name}!")
        
        return redirect('students:course_detail', course_id=course.id)
    
    except StudentProfile.DoesNotExist:
        messages.warning(request, "Please complete your student profile first.")
        return redirect('students:edit_profile')

@login_required
def grades(request):
    """View student grades"""
    try:
        student = request.user.student_profile
        enrollments = Enrollment.objects.filter(student=student)
        
        # Get grades for each enrollment
        grades_data = []
        for enrollment in enrollments:
            try:
                grade = enrollment.grade
                grades_data.append({
                    'course': enrollment.course,
                    'grade': grade.grade,
                    'comments': grade.comments,
                    'graded_date': grade.graded_date,
                })
            except Grade.DoesNotExist:
                grades_data.append({
                    'course': enrollment.course,
                    'grade': 'Not graded yet',
                    'comments': '',
                    'graded_date': None,
                })
        
        context = {
            'title': 'Grades',
            'grades_data': grades_data,
        }
        
        return render(request, 'students/grades.html', context)
    
    except StudentProfile.DoesNotExist:
        messages.warning(request, "Please complete your student profile first.")
        return redirect('students:edit_profile')

@login_required
def attendance(request):
    """View student attendance"""
    try:
        student = request.user.student_profile
        enrollments = Enrollment.objects.filter(student=student)
        
        # Get attendance data for each enrollment
        attendance_data = {}
        attendance_summary = {}
        
        for enrollment in enrollments:
            # Get attendance records for this enrollment
            attendances = Attendance.objects.filter(enrollment=enrollment).order_by('-date')
            
            if attendances.exists():
                # Calculate attendance statistics
                total_classes = attendances.count()
                present_count = attendances.filter(status='present').count()
                absent_count = attendances.filter(status='absent').count()
                late_count = attendances.filter(status='late').count()
                excused_count = attendances.filter(status='excused').count()
                
                # Calculate attendance percentage
                attendance_rate = (present_count + late_count) / total_classes * 100 if total_classes > 0 else 0
                
                # Store attendance summary
                attendance_summary[enrollment.course.id] = {
                    'course': {
                        'id': enrollment.course.id,
                        'code': enrollment.course.code,
                        'name': enrollment.course.name,
                    },
                    'total_classes': total_classes,
                    'present_count': present_count,
                    'absent_count': absent_count,
                    'late_count': late_count,
                    'excused_count': excused_count,
                    'attendance_rate': round(attendance_rate, 2),
                }
                
                # Store attendance records
                attendance_data[enrollment.course.id] = attendances
        
        context = {
            'title': 'Attendance',
            'enrollments': enrollments,
            'attendance_data': attendance_data,
            'attendance_summary': attendance_summary,
            'now': timezone.now(),
        }
        
        return render(request, 'students/attendance.html', context)
    
    except StudentProfile.DoesNotExist:
        messages.warning(request, "Please complete your student profile first.")
        return redirect('students:edit_profile')
