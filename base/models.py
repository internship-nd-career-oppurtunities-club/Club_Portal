from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, Case, When, Value, IntegerField


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255,)
    avatar = models.ImageField(default='avatar.svg', blank=True, null=True)
    banner = models.ImageField(default='banner.jpg', blank=True, null=True)
    membership_choices = [
        ('Student', 'Student'),
        ('Executive Member', 'Executive Member'),
        ('General Secretary', 'General Secretary'),
        ('Joint Secretary', 'Joint Secretary'),
    ]
    role = models.CharField(max_length=20, choices=membership_choices, default='student')
    portfolio = models.URLField(blank=True, null=True)
    resume = models.FileField(blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    Branch_choices = [
        ('Computer Science and Engineering', 'Computer Science and Engineering'),
        ('Electronics and Communication Engineering', 'Electronics and Communication Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Other', 'Other'),
    ]
    branch = models.CharField(max_length=50, choices=Branch_choices, blank=True, null=True)
    passout_year = models.IntegerField(blank=True, null=True)
    semester = models.CharField(blank=True, null=True)


    studentID = models.CharField(max_length=20, blank=True, unique=True, null=True  )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    dob = models.DateField(blank=True, null=True)
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=20, choices=gender_choices, default='NONE')
    address = models.TextField(blank=True, null=True)

    linkedIn = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    # saved_resources = models.ManyToManyField('resources', related_name='saved_resources', blank=True)




class Resources(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type_choices = [
        ('Link/Website', 'Link/Website'),
        ('PDF/Document', 'PDF/Document'),
        ('YT Video', 'YT Video'),
        ('Code Repo', 'Code Repo'),
    ]
    type = models.CharField(max_length=50, choices=type_choices, default='N/A')
    size = models.CharField(max_length=10, default='N/A', null=True)
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=20, blank=True, null=True)
    resourcefile = models.URLField(blank=True, null=True) #Use FileField for uploading files

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    saved_by = models.ManyToManyField('User', related_name='saved_resources', blank=True)

    # class Meta:
    #     order_expression = Case(
    #     *[
    #         When(role='General Secretary', then=Value(0)),
    #         When(role='Joint Secretary', then=Value(1)),
    #         When(role='Executive Member', then=Value(2)),
    #     ],
    #     default=Value(4),
    #     output_field=IntegerField()
    #     )   

    #     ordering = ['order_expression',]

    def __str__(self):
        return self.description[0:100]

class Rounds(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(default=1)
    title = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # activity = models.ForeignKey(Activities, related_name='rounds', on_delete=models.CASCADE)
    resources_included = models.ManyToManyField(Resources, related_name='round_resources', blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Activities(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True) 
    description = models.TextField()
    type = models.CharField(max_length=50, blank=True, null=True)
    banner = models.ImageField(default='banner.jpg', blank=True, null=True)
    status_choices = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Upcoming')
    participants = models.ManyToManyField(User, related_name='activitiesRegistered', blank=True)    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    fromtime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)

    rounds_included = models.ManyToManyField( Rounds, related_name='activity_rounds', blank=True, null=True)
    resources_included = models.ManyToManyField( Resources, related_name='activity_resources', blank=True)
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.description[0:100]
    




    # def __str__(self):
    #     return self.roundname



class ContactUs(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject_choices = [
        ('General Inquiry','General Inquiry'),
        ('Suggestion','Suggestion'),
        ('Collabaration','Collabaration'),
        ('Sponsorship','Sponsorship'),
        ('Resource Request','Resource Request'),
        ('Offer','Offer'),
    ]
    subject = models.CharField(max_length=20, choices=subject_choices, default='General Inquiry')
    message = models.TextField()
