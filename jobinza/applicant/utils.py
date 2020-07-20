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
    #match = list() #m[0]=> matched skills, #m[1]=> not matched skills ,#m[2]=> result
    skills = dict()
    flist  = ""
    ulist  = ""
    found= 0
    for i in hrSkills:
        if i in AppSkills:
            found=found+1
            flist =flist+ i + " - "
        else:
            ulist =ulist+ i + " - "
    prc = Percent(found,hrSkills)
    skills = {'fnd':flist[:-2],'nfnd':ulist[:-2],'percent':prc}
    return skills

def IsFileExists(filename):
    if filename == os.listdir(settings.MEDIA_ROOT):
        return True
    return False
