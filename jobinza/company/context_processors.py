from company.models import CreatePost
# this file for search field and need alot to be accurate
def add_variable_to_context(request):
    posts = CreatePost.objects.all()
    lst = list()
    for i in posts:
        lst.append(i.jobtitle)

    return {
        'jobs': 'walid'
    }