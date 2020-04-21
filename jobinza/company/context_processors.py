from company.models import CreatePost , Notification

# this file for search field and need alot to be accurate
def add_variable_to_context(request):
    posts = CreatePost.objects.all()
    lst = list()
    for i in posts:
        lst.append(i.jobtitle)

    return {
        'jobs': 'walid'
    }

def list_Notification(request):
    count = 0
    Notification_list = Notification.objects.all().filter(receiver= request.user.id).order_by('id').reverse()
    for n in Notification_list :
        if n.read == False :
            count = count +1


    return {'notifications':Notification_list , 'count' : count }        

   
