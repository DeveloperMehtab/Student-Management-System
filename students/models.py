from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cryptography.fernet import Fernet
import base64
import os
from django.conf import settings

# Encryption key management
def get_encryption_key():
    """Get or generate an encryption key for sensitive data"""
    key_file = os.path.join(settings.BASE_DIR, '.encryption_key')
    
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
    
    return key

# Encryption mixin for models
class EncryptedFieldMixin:
    """Mixin to provide encryption/decryption for model fields"""
    
    def encrypt_value(self, value):
        if not value:
            return value
        
        if isinstance(value, str):
            value = value.encode('utf-8')
        
        f = Fernet(get_encryption_key())
        encrypted_value = f.encrypt(value)
        return base64.b64encode(encrypted_value).decode('utf-8')
    
    def decrypt_value(self, value):
        if not value:
            return value
        
        try:
            f = Fernet(get_encryption_key())
            decrypted_value = f.decrypt(base64.b64decode(value))
            return decrypted_value.decode('utf-8')
        except Exception:
            return "Decryption Error"

# Student Profile model
class StudentProfile(models.Model, EncryptedFieldMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    _address = models.TextField(db_column='address', blank=True)  # Encrypted field
    _phone_number = models.CharField(db_column='phone_number', max_length=255, blank=True)  # Encrypted field
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def address(self):
        return self.decrypt_value(self._address)
    
    @address.setter
    def address(self, value):
        self._address = self.encrypt_value(value)
    
    @property
    def phone_number(self):
        return self.decrypt_value(self._phone_number)
    
    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = self.encrypt_value(value)
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

# Course model
class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.PositiveIntegerField(default=3)
    instructor = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

# Enrollment model
class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.user.username} - {self.course.code}"

# Grade model
class Grade(models.Model, EncryptedFieldMixin):
    GRADE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
    )
    
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='grade')
    _grade = models.CharField(db_column='grade', max_length=255)  # Encrypted field
    _comments = models.TextField(db_column='comments', blank=True)  # Encrypted field
    graded_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def grade(self):
        return self.decrypt_value(self._grade)
    
    @grade.setter
    def grade(self, value):
        self._grade = self.encrypt_value(value)
    
    @property
    def comments(self):
        return self.decrypt_value(self._comments)
    
    @comments.setter
    def comments(self, value):
        self._comments = self.encrypt_value(value)
    
    def __str__(self):
        return f"{self.enrollment.student.user.username} - {self.enrollment.course.code} - {self.grade}"

# Attendance model
class Attendance(models.Model, EncryptedFieldMixin):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    _remarks = models.TextField(db_column='remarks', blank=True)  # Encrypted field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('enrollment', 'date')
        ordering = ['-date']
    
    @property
    def remarks(self):
        return self.decrypt_value(self._remarks)
    
    @remarks.setter
    def remarks(self, value):
        self._remarks = self.encrypt_value(value)
    
    def __str__(self):
        return f"{self.enrollment.student.user.username} - {self.enrollment.course.code} - {self.date} - {self.status}"

# Notification model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
