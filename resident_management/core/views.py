from django.shortcuts import render

def dashboard_view(request):
    """
    Render giao diện Dashboard chính.
    """
    return render(request, 'dashboard.html')

