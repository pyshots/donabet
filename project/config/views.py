from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

def prueba_template(request):
    mi_html = open("./templates/template1.html")
    mi_template = Template(mi_html.read())
    mi_html.close()
    mi_contexto = Context({"nombre": "el consexo"})
    mi_documento = mi_template.render(mi_contexto)
    return HttpResponse(mi_documento)

def mis_notas(request):
    return render(request, "notas.html")