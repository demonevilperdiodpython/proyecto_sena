"""Comando de Django: manage.py check_comentarios

Comprueba que ningun comentario {# ... #} este partido en varias lineas, que
es lo que hace que se impriman en la pagina (ver el comentario del modulo)."""
from django.core.management.base import BaseCommand

# checks_comentarios.py vive en apps/catalog/, un nivel por encima de este
# paquete, asi que el import tiene que ser absoluto.
from apps.catalog.checks_comentarios import revisar


class Command(BaseCommand):
    help = "Revisa que ningun comentario de plantilla se imprima en la pagina."

    def handle(self, *args, **options):
        fugados = revisar()
        if fugados:
            self.stderr.write(
                self.style.ERROR(
                    "{} comentario(s) se imprimen en la pagina: "
                    "ponlos en una sola linea.".format(len(fugados))
                )
            )
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS("Plantillas revisadas."))