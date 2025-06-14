# Generated by Django 5.1.7 on 2025-03-10 16:22

import django.db.models.deletion
import students.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('excused', 'Excused')], max_length=10)),
                ('_remarks', models.TextField(blank=True, db_column='remarks')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='students.enrollment')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('enrollment', 'date')},
            },
            bases=(models.Model, students.models.EncryptedFieldMixin),
        ),
    ]
