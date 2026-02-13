from multiprocessing.dummy import Value
from django.shortcuts import render, redirect

from .models import User, Activities, Rounds, Resources
from django.forms.models import model_to_dict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm, AddResourceForm, ContactUsForm

# from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q, Case, When, Value, IntegerField, Count

from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings





# Create your views here.
def home(request):
    activities = Activities.objects.annotate(participants_count = Count('participants')).order_by('-participants_count')[:3]
    print(activities)
    context = {'activities': activities}
    return render(request, 'base/home.html', context)



def profile(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    user = User.objects.get(username=pk)
    
    context = {'user': user}
    return render(request, 'base/profile.html', context)



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    context = {'page' : 'login'}
    return render(request, 'base/login_register.html', context)



def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse(form.errors)

    context = {'page' : 'register', 'form': form}
    return render(request, 'base/login_register.html', context)



@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserProfileForm(instance=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.username)
        else:
            return HttpResponse(form.errors)

    context = {'form': form}
    return render(request, 'base/update-profile.html', context)



@login_required(login_url='login')
def logoutPage(request):
    logout(request)

    context = {}
    return render(request, 'base/home.html', context)



def membersPage(request):
    order_expression = Case(
        *[
            When(role='General Secretary', then=Value(0)),
            When(role='Joint Secretary', then=Value(1)),
            When(role='Executive Member', then=Value(2)),
        ],
        default=Value(4),
        output_field=IntegerField()
    )
    members = User.objects.filter(role__in=['General Secretary', 'Joint Secretary', 'Executive Member']).order_by(order_expression)

    context = {'members': members,}
    return render(request, 'base/members.html', context)



def quickview(request, pk):
    member = User.objects.get(username=pk)
    context = {'member': member}
    return render(request, 'quickview.html', context)



def activitiesPage(request):
    status = request.GET.get('status') 
    
    if status == 'Upcoming':        
        activities = Activities.objects.filter(status = 'Upcoming')
    elif status == 'Completed': 
        activities = Activities.objects.filter(status = 'Completed')
    else:
        activities = Activities.objects.all()

    # 'pastActivities' : pastActivities
    context = {'activities': activities,'status':status}
    return render(request, 'base/activities.html', context)



def activity(request, pk):
    activity = Activities.objects.get(id=pk)
    # rounds = Rounds.objects.filter(activity=activity)
    rounds = activity.rounds_included.all()
    activityResources = activity.resources_included.all()

    if request.method == 'POST':
        if request.user.is_authenticated:   
            activity.participants.add(request.user)
            return redirect('activity', pk=activity.id )
        else:
            return redirect('login')

    context = {'activity': activity, 'rounds': rounds, 'activityResources': activityResources}
    return render(request, 'base/activity.html', context)


@login_required(login_url='login')
def newActivity(request):
    context = {}
    return render(request, 'base/new_activity_form.html', context)


def resourcesPage(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    resources = Resources.objects.filter( Q(name__icontains=search) | Q(description__icontains=search) | Q(tags__icontains=search) | Q(type__icontains=search) )

    
    saved = request.GET.get('saved') if request.GET.get('saved') != None else ''
    if saved == 'True' and request.user.is_authenticated:
        resources = Resources.objects.filter(saved_by__name=request.user.name)

    context = {'resources':resources, 'saved':saved, }
    return render(request, 'base/resources.html', context)


@login_required(login_url='login')
def saveResource(request,pk):
    resource = Resources.objects.get(id=pk)

    if request.user.is_authenticated :
        if request.user not in resource.saved_by.all():
            # user = request.user
            # user.saved_resources.add(resource)
            resource.saved_by.add(request.user)
            return redirect('resources')
        else:
            resource.saved_by.remove(request.user)
            return redirect('resources')
    else:
        return redirect('login')


@login_required(login_url='login')
def addResource(request):
    form = AddResourceForm()

    if request.method == 'POST':
        form = AddResourceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('resources')
        else:
                return HttpResponse("An error occurred while updating the profile")
    
    context = {'form':form,}
    return render(request, 'base/new_resource_form.html', context)

    

def contactUsPage(request):
    form = ContactUsForm()



    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # send_mail(
            #     "Confirmation: We have received your message",
            #     f"Hi {name},\nWe have received your message regarding {subject}.\n\nThank you for reaching out to Internships and Oppurtunities Club, Rgukt Sklm. We appreciate the interest you have in our Club. We will get back to you as soon as possible.",
            #     settings.ADMIN_EMAIL,
            #     [email,], # To email                  
            #     fail_silently=False,
            # )

            # send_mail(
            #     f"Contact Us Request from {name} regarding {subject}",
            #     message,
            #     email,
            #     [settings.ADMIN_EMAIL],                             
            #     fail_silently=False,
            # )



            # message1 = (
            #     "Confirmation: We have received your message",
            #     f"Hi {name},\nWe have received your message regarding {subject}.\n\nThank you for reaching out to Internships and Oppurtunities Club, Rgukt Sklm. We appreciate the interest you have in our Club. We will get back to you as soon as possible.",
            #     settings.ADMIN_EMAIL,
            #     [email,], # To email                  
            # )
            # message2 = (
            #     f"Contact Us Request from {name} regarding {subject}",
            #     f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}</span> ",
            #     email,
            #     [settings.ADMIN_EMAIL],  
            # )
            # send_mass_mail((message1, message2), fail_silently=False)


            # email = EmailMessage(
            #     "Email Subject",
            #     "Body of email goes here",
            #     "from@example.com",
            #     ["recipient@example.com", ],
            #     ["bcc@example.com"],
            #     reply_to=["paulie@example.com"],
            #     headers={"Message-ID": "foo"},
            # )

            html_message = render_to_string('base/emails/confirmation.html', {
                'name': name,
            })
            # plain_message = strip_tags(html_message)
            
            email = EmailMessage(
                subject= "Confirmation: We have received your message",
                body= html_message,
                from_email= settings.ADMIN_EMAIL,
                to=[user_email,],
                reply_to=[settings.ADMIN_EMAIL],
            )
            email.content_subtype = 'html'  # This tells Django to send HTML email
            email.send()


            #Notify Admin
            html_message = render_to_string('base/emails/notify.html', {
                'name': name,
                'email': user_email,
                'subject': subject,
                'message': message,
            })
            # plain_message = strip_tags(html_message)
            
            email = EmailMessage(
                subject= "Contact Us Request from {0} regarding {1}".format(name, subject),
                body= html_message,
                from_email= settings.ADMIN_EMAIL,
                to=[settings.ADMIN_EMAIL,],
                reply_to=[user_email,],
            )
            email.content_subtype = 'html'  # This tells Django to send HTML email
            email.send()




            # subject = "Your OTP Code"
            # text_content = f"Your OTP is {otp}."
            # html_content = f"<p>Your OTP is <strong>{otp}</strong></p>"
            # msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user_email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            form.save()
            return redirect('home')  
        else:
            return HttpResponse(form.errors)

    context = {'form':form}
    return render(request, 'base/contact_us.html', context)



def devPage(request):
    context = {}
    return render(request, 'base/dev.html', context)