# from django.http import HttpResponseRedirect

# def login_redirect_required(request):

#     def decorator(function):

#         def wrapper(request, *args, **kwargs):
#             if request.user.is_authenticated:
#                 return function(request, *args, **kwargs)
#             return HttpResponseRedirect('singin/?next=' + request.path)

#         return wrapper

#     return decorator
