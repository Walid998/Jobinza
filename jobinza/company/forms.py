from django import forms

from company.models import CreatePost,Match_Results,Send_Email,Schdule
from account.models import Profile
from datetime import datetime



class editprofileForm(forms.ModelForm):
    #image = forms.ImageField(required=False)
    phonenumber = forms.CharField(required=False)
    address = forms.CharField(required=False)
    location = forms.CharField(required=False)
    description = forms.CharField(required=False)
    

    class Meta:
        model = Profile
        fields = [
	
        #'image',
        'phonenumber',
        'address',
        'location', 
        'description',			

]




class CreatePostForm(forms.ModelForm):

	class Meta:
		model = CreatePost
		fields = [
	
        'jobtitle', 			
        'joblocation',         
        'city',     			
        'Area',    			
        'careerlevel', 		
        'year_of_experience', 	
        'salary_range1',
        'salary_range2', 		
        'num_vacancies', 		
        #'rolejob', 			
        #'related_industry', 	
        'jobtype',			
        'job_description', 	
        'skills', 				
        'deadline',
        'image',
        'category',
]

class SendEmailForm(forms.Form):
    class Meta:
        model : Send_Email
        fields = [
            'username',
            'email',
            'content',
        ]
class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

class SchduleForm(forms.Form):
    class Meta:
        model : Schdule
        fields = ['username','jobname','date_schdule','time_schdule',]