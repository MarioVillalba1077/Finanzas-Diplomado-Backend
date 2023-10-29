from django.shortcuts import render, get_object_or_404, redirect
from .models import Persona
from .forms import PersonaForm

def listar_personas(request):
    personas = Persona.objects.all()
    return render(request, 'listar_personas.html', {'personas': personas})

def buscar_personas(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        numero_documento = request.POST.get('numero_documento', '')
        personas = Persona.objects.filter(nombre__icontains=nombre, numero_documento__icontains=numero_documento)
    else:
        personas = Persona.objects.all()
    return render(request, 'buscar_personas.html', {'personas': personas})

def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_personas')
    else:
        form = PersonaForm()
    return render(request, 'crear_persona.html', {'form': form})


def editar_eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        
        if 'editar' in request.POST:  # Si se hace clic en el botón 'Editar'
            if form.is_valid():
                form.save()
                return redirect('listar_personas')
        elif 'eliminar' in request.POST:  # Si se hace clic en el botón 'Eliminar'
            persona.delete()
            return redirect('listar_personas')
    else:
        form = PersonaForm(instance=persona)
    
    return render(request, 'editar_eliminar_persona.html', {'form': form, 'persona': persona})


