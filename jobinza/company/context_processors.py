from company.models import CreatePost
from notify.signals import notify

# this file for search field and need alot to be accurate
def add_variable_to_context(request):
    posts = CreatePost.objects.all()
    lst = list()
    for i in posts:
        lst.append(i.jobtitle)

    return {
        'jobs': 'walid'
    }

def notifications(request):
	count = 0
	notification_list = request.user.notifications.active().prefetch()
	for n in notification_list:
		if n.read == False:
			count = count+1
	return {'notifications': notification_list , 'count':count }
