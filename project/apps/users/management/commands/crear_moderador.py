from getpass import getpass

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

from apps.users.models import customuser


class Command(BaseCommand):
    help = "Crea o promueve un moderador global (is_platform_admin=True)."

    def add_arguments(self, parser):
        parser.add_argument("username", nargs="?", help="Usuario existente o nuevo.")
        parser.add_argument("--email", help="Email del usuario nuevo.")
        parser.add_argument("--password", help="Contrasena del usuario nuevo.")
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="No pedir datos por consola. Requiere --email y --password si el usuario no existe.",
        )
        parser.add_argument(
            "--remove",
            action="store_true",
            help="Quita el rol de moderador global.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        if not username:
            if options["noinput"]:
                raise CommandError("Debes indicar el nombre de usuario.")
            username = input("Usuario: ").strip()
        if not username:
            raise CommandError("Debes indicar un nombre de usuario.")

        try:
            user = customuser.objects.get(username=username)
        except customuser.DoesNotExist:
            if options["remove"]:
                raise CommandError("El usuario no existe.")

            email = options["email"]
            if not email:
                if options["noinput"]:
                    raise CommandError("Debes indicar --email para crear el usuario.")
                email = input("Email (@gmail.com): ").strip()
            if not email:
                raise CommandError("El email es obligatorio.")
            try:
                validate_email(email)
            except ValidationError:
                raise CommandError("El email no es valido.")
            if not email.lower().endswith("@gmail.com"):
                raise CommandError("El email debe ser @gmail.com.")

            password = options["password"]
            if not password:
                if options["noinput"]:
                    raise CommandError("Debes indicar --password para crear el usuario.")
                password = getpass("Contrasena: ")
                if not password:
                    raise CommandError("La contrasena no puede estar vacia.")

            user = customuser.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(f"Usuario {username} creado."))

        if options["remove"]:
            user.is_platform_admin = False
            user.save(update_fields=["is_platform_admin"])
            self.stdout.write(
                self.style.SUCCESS(f"{username} ya no es moderador global.")
            )
            return

        if getattr(user, "is_banned", False) or not user.is_active:
            raise CommandError(
                "El usuario esta suspendido o inactivo. Reactivalo antes de darle el rol."
            )

        user.is_platform_admin = True
        user.save(update_fields=["is_platform_admin"])
        self.stdout.write(
            self.style.SUCCESS(f"{username} ahora es moderador global.")
        )
