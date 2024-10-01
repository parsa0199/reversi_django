from django.shortcuts import render

def reversi_view(request):
    return render(request, 'reversi/reversi.html')
