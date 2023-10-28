from django.shortcuts import render, redirect
from .models import Persona
from .forms import PersonaForm

def listar_personas(request):
    personas = Persona.objects.all()
    return render(request, 'listar_personas.html', {'personas': personas})

# def buscar_personas(request):
#     if request.method == 'POST':
#         nombre = request.POST.get('nombre', '')
#         numero_documento = request.POST.get('numero_documento', '')
#         personas = Persona.objects.filter(nombre__icontains=nombre, documento__icontains=numero_documento)
#     else:
#         personas = Persona.objects.all()
#     return render(request, 'buscar_personas.html', {'personas': personas})

def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_personas')
    else:
        form = PersonaForm()
    return render(request, 'crear_persona.html', {'form': form})

