from django.http import JsonResponse

def hendler404(request, exception):
    message = ('Route not found')
    response = JsonResponse(data={"error": message})
    response.status_code = 404
    return response

def hendler500(request):
    message = ('Internal server error')
    response = JsonResponse(data={"error": message})
    response.status_code = 500
    return response
