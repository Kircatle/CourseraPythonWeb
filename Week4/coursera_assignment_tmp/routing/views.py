from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt


def simple_route(request):
    if request.method == "GET":
        return HttpResponse(status="200") 
    else:
        return HttpResponse(status="405") 


def slug_route(request, slug):
    return HttpResponse(slug, status="200")


def sum_route(request, num1, num2):
    return HttpResponse(int(num1)+int(num2), status="200") 


@require_GET
def sum_get_method(request):
    try:
        a = request.POST['a']
        b = request.POST['b']
        return HttpResponse(int(a)+int(b), status="200")
    except ValueError:
        return HttpResponse(status="400") 
    except KeyError:
        return HttpResponse(status="400") 


@csrf_exempt
@require_POST
def sum_post_method(request):
    try:
        a = request.POST['a']
        b = request.POST['b']
        return HttpResponse(int(a)+int(b), status="200")
    except ValueError:
        return HttpResponse(status="400") 
    except KeyError:
        return HttpResponse(status="400") 


