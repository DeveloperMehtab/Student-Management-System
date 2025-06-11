from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile, Course, Enrollment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class StudentProfileForm(forms.ModelForm):
    student_id = forms.CharField(max_length=20, required=True, help_text="Enter your student ID")
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )
    phone_number = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'date_of_birth', 'address', 'phone_number', 'profile_picture']
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if StudentProfile.objects.filter(student_id=student_id).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError("This student ID is already in use.")
        return student_id

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a course"
    )
    
    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        
        if self.student:
            # Exclude courses the student is already enrolled in
            enrolled_courses = Enrollment.objects.filter(
                student=self.student
            ).values_list('course_id', flat=True)
            self.fields['course'].queryset = Course.objects.exclude(
                id__in=enrolled_courses
            ) 