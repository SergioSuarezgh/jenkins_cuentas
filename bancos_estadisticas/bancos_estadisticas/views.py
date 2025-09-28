from django.shortcuts import render


def cargar_index(request):
    return render(request, "index.html")
