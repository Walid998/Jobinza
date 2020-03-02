from django.shortcuts import render

# Create your views here.
def job_details(request):
    return render(request,'applicant/job_details.html')