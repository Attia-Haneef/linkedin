from django.contrib import auth
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator

# Create your models here.
class Company(models.Model):
    TYPE_CHOICES = (
        ('CS/IT', 'CS/IT'),
        ('Charted Accounted','Charted Accounted'),
        ('Digital Marketing', 'Digital Marketing'),
        ('Digital Content', 'Digital Content'),
        ('Data Sciences', 'Data Sciences'),
        ('Business Developmemt and Sales', 'Buisness Development and Sales'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    join_date = models.DateField()
    type = models.CharField(max_length=50, choices= TYPE_CHOICES, default='CS/IT')
    establish_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f'{self.title}'


class Skill(models.Model):
    title = models.CharField(max_length=200, unique=True)


    def __str__(self):
        return self.title


class Education(models.Model):   
    title = models.CharField(max_length=200)
   

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    join_date = models.DateField()
    birth_date = models.DateField(max_length=8)
    skills = models.ManyToManyField(Skill)
    connections = models.ManyToManyField('self', symmetrical=False,through='Connection', blank=True)
    educations = models.ManyToManyField(Education, through='MemberEducation', blank=True )
    joined_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'^\+?92?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")], max_length=17, blank=True) 
    job_position = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MemberEducation(models.Model):
    INSTITUTE_CHOICES = (
        ('Punjab Clg', 'Punjab Clg'),
        ('Fast Nuces','Fast Nuces'),
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    institute = models.CharField(max_length=50, choices=INSTITUTE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()



class Connection(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Connected','Connected'),
    )
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')


class PositionVersion(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    job_position = models.CharField(max_length=200)


class Endorsment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='endorsements')
    endorsed_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='endorsed_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.endorse} endorse {self.endorsed} skill'

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f'{self.title}'