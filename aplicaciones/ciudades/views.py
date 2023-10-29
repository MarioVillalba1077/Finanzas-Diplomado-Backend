from django.shortcuts import render, get_object_or_404, redirect
from .models import Ciudad
from .forms import CiudadForm

def listar_ciudades(request):
    ciudades = Ciudad.objects.all()
    return render(request, 'listar_ciudades.html', {'ciudades': ciudades})

def buscar_ciudades(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        departamento = request.POST.get('departamento', '')
        ciudades = Ciudad.objects.filter(nombre__icontains=nombre, departamento__icontains=departamento)
    else:
        ciudades = Ciudad.objects.all()
    return render(request, 'buscar_ciudades.html', {'ciudades': ciudades})

def crear_ciudad(request):
    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_ciudades')
    else:
        form = CiudadForm()
    return render(request, 'crear_ciudad.html', {'form': form})


def editar_eliminar_ciudad(request, ciudad_id):
    ciudad = get_object_or_404(Ciudad, pk=ciudad_id)
    
    if request.method == 'POST':
        form = CiudadForm(request.POST, instance=ciudad)
        
        if 'editar' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('listar_ciudades')
        elif 'eliminar' in request.POST:
            ciudad.delete()
            return redirect('listar_ciudades')
    else:
        form = CiudadForm(instance=ciudad)
    
    return render(request, 'editar_eliminar_persona.html', {'form': form, 'ciudad': ciudad})
