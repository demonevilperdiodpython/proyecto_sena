"""Chequeo rapido: comentarios de plantilla que se IMPRIMEN en la pagina.

Django 6.1 tokeniza con re.compile(r"({%.*?%}|{{.*?}}|{#.*?#})") SIN
re.DOTALL, asi que un {# ... #} partido en varias lineas no se reconoce como
comentario y sale escrito en el HTML.

Uso:  manage.py check_comentarios
Salida: codigo 1 si queda alguno.
"""
import re
from pathlib import Path

from django.conf import settings

PATRON = re.compile(r"\{#(.*?)#\}", re.S)
BASE = Path(settings.BASE_DIR).parent


def comentarios_fugados():
    """Devuelve [(archivo, linea)] de los comentarios de varias lineas."""
    salida = []
    for plantilla in BASE.rglob("*.html"):
        partes = str(plantilla)
        if "site-packages" in partes or "\\venv\\" in partes or "\\migrations\\" in partes:
            continue
        texto = plantilla.read_text(encoding="utf-8", errors="replace")
        for encontrado in PATRON.finditer(texto):
            if "\n" in encontrado.group(1):
                linea = texto[:encontrado.start()].count("\n") + 1
                salida.append((plantilla.relative_to(BASE), linea))
    return salida


def revisar():
    fugados = comentarios_fugados()
    # Ojo: las llaves van en doble ({{ ... }}) porque str.format leeria
    # "{#" como el principio de un campo y saltaria con KeyError.
    for archivo, linea in fugados:
        print("{}  L{}  este comentario {{# ... #}} esta en varias lineas "
              "y sale impreso en la pagina".format(archivo, linea))
    if not fugados:
        print("Ningún comentario se imprime en la pagina.")
    return fugados