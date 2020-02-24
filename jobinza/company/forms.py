from django import forms

from company.models import CreatePost


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
        'salary_range', 		
        'additional_salary', 	
        'num_vacancies', 		
        'rolejob', 			
        'related_industry', 	
        'jobtype',			
        'job_description', 	
        'skills', 				
        'image', 				


]

