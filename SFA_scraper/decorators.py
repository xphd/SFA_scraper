from django.http import HttpResponse
from django.shortcuts import render

def user_is_manager(function):
    def wrap(request, *args, **kwargs):
        level = request.user.profile.access_level
        if level == 'Management':
            return function(request, *args, **kwargs)
        else:
            return render(request, 'main.html', {'message': 'Sorry, you do not have permission as ' + level})
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_searcher(function):
    def wrap(request, *args, **kwargs):
        level = request.user.profile.access_level
        if level == 'Management' or level == 'Searcher':
            return function(request, *args, **kwargs)
        else:
            return render(request, 'main.html', {'message': 'Sorry, you do not have permission as ' + level})
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap