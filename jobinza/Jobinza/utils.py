from django.core.paginator import Paginator

def PaginatorX(request,anyList,itemsToList):
    paginator = Paginator(anyList,itemsToList)
    page = request.GET.get('page')
    return paginator.get_page(page)