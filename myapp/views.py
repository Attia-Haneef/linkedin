from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from myapp.forms import ConnectionViewForm, NewUserForm, LoginForm
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib import messages
from django.views.generic import View, CreateView
from myapp.models import Member,  Connection, Job
from django.db.models import Q
from myapp.forms import AddMemberForm, AddCompanyForm, MemberSkillForm, AddJobForm, AddEducationForm, MakeConnections, ViewConnections, AddEndorsementForm, ConnectionViewForm


def register_request(request):
    if request.method == 'GET':
        return render(request, 'myapp/register.html', context={'register_form': NewUserForm()})

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_user(request, user)
            messages.success(request, 'Registration successful.')
            if request.POST['user_type'] == 'Member':             
                return redirect('myapp:addmember')
            else:
                return redirect('myapp:addcompany')
        return render(request, 'myapp/register.html', context={'register_form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'myapp/login.html', context={'form': LoginForm()})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username= request.POST['username'], password=request.POST['password'])
            if user is not None:
                login_user(request, user)
                messages.success(request, 'Login Successful')
                return redirect('myapp:homepage')
        messages.error(request, 'Invalid username or password')
        return render(request, 'myapp/login.html', context={'form': form})


def logout(request):
    logout_user(request)
    return redirect('myapp:login')


class MemberCreateView(CreateView):
    form_class = AddMemberForm
    template_name = 'myapp/addmember.html'
    success_url = reverse_lazy('myapp:homepage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CompanyCreateView(CreateView):
    form_class = AddCompanyForm
    template_name = 'myapp/addcompany.html'
    success_url = reverse_lazy('myapp:homepage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('myapp:login')

        jobs = []
        member_skills_set = set(request.user.member.skills.values_list('id', flat=True))
        print(member_skills_set)
        for job in Job.objects.all():
            skills_set = set(job.skills.values_list('id', flat=True))
            if skills_set.issubset(member_skills_set):
                jobs.append(job)
        return render(request, 'myapp/homepage.html', context={'jobs': jobs})


class MemberSkillView(View):
    def get(self, request):
        return render(request, 'myapp/memberskill.html', context={'form': MemberSkillForm(instance=request.user.member)})
    
    def post(self, request):
        form = MemberSkillForm(request.POST, instance=request.user.member)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {request.user.member} Skills successfully')
            return redirect('myapp:homepage')
        return render(request, 'myapp/memberskill.html', context={'form':form})


class JobCreateView(CreateView):
    form_class = AddJobForm
    template_name = 'myapp/addjob.html'
    success_url = reverse_lazy('myapp:homepage')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)


class EducationCreateView(CreateView):
    form_class = AddEducationForm
    template_name = 'myapp/addeducation.html'
    success_url = reverse_lazy('myapp:homepage')

    def form_valid(self, form):
        form.instance.member = self.request.user.member
        return super().form_valid(form)


class ConnectionCreateView(View):
    def get(self, request):
        return render(request, 'myapp/makeconnection.html', context={'form': MakeConnections(instance=request.user.member)})
    
    def post(self, request):
        form = MakeConnections(request.POST, instance=request.user.member)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {request.user.member} Connections successfully')
            return redirect('myapp:homepage')
        return render(request, 'myapp/makeconnection.html', context={'form':form})

class ConnectionConfirmView(View):
    def get(self, request):
        connection_list = Connection.objects.filter(receiver=request.user.member,status='pending')
        context = {
            'form': ViewConnections(instance=request.user.member),
            'connection_list': connection_list
        }
        return render(request, 'myapp/viewconnection.html', context)

def connect(request, connection_id=id):
    connected = Connection.objects.filter(sender_id=connection_id, receiver_id=request.user.member)
    connected.update(status='Connected')
    return redirect('myapp:homepage')


class UpdateProfileView(View):
    def get(self, request):
        return render(request, 'myapp/updatemember.html', context={'form': AddMemberForm(instance=request.user.member )})

    def post(self, request):
        form = AddMemberForm(request.POST, instance=request.user.member)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {request.user.member} Profile successfully')
            return redirect('myapp:homepage')
        return render(request, 'myapp/updatemember.html', context={'form':form})

class UpdateCompanyView(View):
    def get(self, request):
        return render(request, 'myapp/updatecompany.html', context={'form': AddCompanyForm(instance=request.user.company )})

    def post(self, request):
        form = AddCompanyForm(request.POST, instance=request.user.company)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {request.user.company} Profile successfully')
            return redirect('myapp:homepage')
        return render(request, 'myapp/updatecompany.html', context={'form':form})


class EndorsementView(View):
    def get(self, request, member_id):
        return render(request, 'myapp/endorseskill.html', context={'form': AddEndorsementForm(member_id=member_id, endorser=request.user.member)})
    
    def post(self, request, member_id):
        form = AddEndorsementForm(request.POST, member_id=member_id, endorser=request.user.member)
        form.instance.member = Member.objects.get(id=member_id)
        form.instance.endorsed_by = request.user.member
        if form.is_valid():
            form.save()
            return redirect('myapp:homepage')
        return render(request, 'myapp/endorseskill.html', context={'form': form})


class DisplayConnections(View):
    def get(self, request):
        context = {
            'form': ConnectionViewForm(instance=request.user.member),
            'connected_members' : Connection.objects.filter((Q(receiver=request.user.member) | Q(sender=request.user.member)), status='connected'),
        }
        return render(request, 'myapp/connected.html', context=context)
