from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Company, Connection, Education, Endorsment, Job, Member, MemberEducation


class NewUserForm(UserCreationForm):
    USER_CHOICES = (
        ('Company', 'Company'),
        ('Member', 'Member')
    )
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2","user_type")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class DateInput(forms.DateInput):
    input_type = 'date'


class AddMemberForm(ModelForm):
    class Meta:
         model = Member
         exclude = ('user', 'skills', 'connections', 'educations')
         widgets = {
            'join_date': DateInput(),
            'birth_date': DateInput()
         }

class AddCompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)
        widgets = {
            'join_date': DateInput(),
            'establish_date': DateInput()
        }


class MemberSkillForm(ModelForm):
    class Meta:
        model = Member
        fields = ('skills',)
        widgets = {
            'skills': forms.CheckboxSelectMultiple()
        }


class AddEducationForm(ModelForm):
    class Meta:
        model = MemberEducation
        exclude = ('member',)
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
         }


class AddJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ('company',)
        widgets = {
            'skills': forms.CheckboxSelectMultiple()
        }
        

class MakeConnections(ModelForm):
    class Meta:
        model = Member
        fields = ('connections',)
        widgets = {
            'connections': forms.CheckboxSelectMultiple()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['connections'].queryset = Member.objects.exclude(id=kwargs['instance'].id)

class ViewConnections(ModelForm):
    class Meta:
        model = Connection
        fields = '__all__'


class AddEndorsementForm(ModelForm):
    class Meta:
        model = Endorsment
        exclude = ('endorsed_by',)
    
    def __init__(self, *args, **kwargs):
        member_obj = kwargs.pop('member', None)
        super().__init__(*args, **kwargs)
        if member_obj:
            self.fields['member'].queryset = member_obj.connections.filter(receiver__status='Connected')
