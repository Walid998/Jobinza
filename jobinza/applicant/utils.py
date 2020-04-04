import os
from django.conf import settings 
def Percent(number,List):
    percent = 0
    try:
        percent = f'{(number/len(List))*100.00:.2f}'
    except:
        print('>>> wrong in percent function')
    return percent

def Comparison(hrSkills,AppSkills):
    found= 0
    for i in hrSkills:
        if i in AppSkills:
            found=found+1
    return Percent(found,hrSkills)

def IsFileExists(filename):
    if filename == os.listdir(settings.MEDIA_ROOT):
        return True
    return False
