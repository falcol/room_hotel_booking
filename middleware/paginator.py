from decouple import config
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginator_list_function(list, page_number):
    paginator = Paginator(list, config("ELEMENTS_PER_PAGE"))

    try:
        paginator_list = paginator.page(page_number)
    except PageNotAnInteger:
        paginator_list = paginator.page(config("FIRST_PAGE"))
    except EmptyPage:
        paginator_list = paginator.page(paginator.num_pages)

    return paginator_list
