from django import forms

from company.models import CreatePost
from datetime import datetime


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

]


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )