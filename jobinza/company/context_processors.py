from company.models import CreatePost , Notification
from account.models import Profile
# this file for search field and need alot to be accurate
def add_variable_to_context(request):
    pic = None
    try:
        obj =Profile.objects.get(author = request.user.id)
        if obj.image != "" or obj.image is not None:
            pic = obj.image 
    except:
        pic = None
    return {
        'usr_prof_pic': pic
    }

def list_Notification(request):
    count = 0
    Notification_list = Notification.objects.all().filter(receiver= request.user.id).order_by('id').reverse()
    for n in Notification_list :
        if n.read == False :
            count = count +1


    return {'notifications':Notification_list , 'count' : count }        

   
