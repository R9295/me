from django.shortcuts import render


def handler404(request, exception):
    data = {
        'user': request.user.__str__,
    }
    return render(request, 'errors/404.html', data, status=404)


def handler500(request):
    data = {
        'user': request.user.__str__,
    }
    return render(request, 'errors/500.html', data, status=500)


def handler403(request):
    # no need for bug report here as there's a good reason for a 403
    return render(request, 'errors/403.html', status=403)


def handler400(request, exception):
    data = {
        'user': request.user.__str__,
    }
    return render(request, 'errors/400.html', data, status=400)
