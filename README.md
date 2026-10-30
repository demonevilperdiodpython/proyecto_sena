# Proyecto SENA

Plataforma web desarrollada en Django con autenticación social, catálogo de contenido, pedidos y funcionalidades asistidas por inteligencia artificial (Ollama).

## Repositorio Oficial
- GitHub: [https://github.com/demonevilperdiodpython/proyecto_sena](https://github.com/demonevilperdiodpython/proyecto_sena)

---

## Estructura del Proyecto

```text
proyecto_sena/
├── project/
│   ├── apps/
│   │   ├── catalog/     # Catálogo de temas, publicaciones e interacción
│   │   ├── orders/      # Gestión de pedidos
│   │   └── users/       # Usuarios, perfiles y autenticación personalizada
│   ├── project/         # Configuración central (settings, urls, wsgi, asgi)
│   ├── static/          # Archivos estáticos globales
│   ├── templates/       # Plantillas base globales
│   └── manage.py
├── .env.example         # Ejemplo de variables de entorno
├── .gitignore           # Reglas de exclusión de Git
└── requirements.txt     # Dependencias del proyecto
```

---

## Requisitos Previos

- Python 3.11+
- Virtualenv o venv
- (Opcional) XAMPP / MariaDB / MySQL si no se utiliza SQLite
- (Opcional) Servidor Ollama local para funciones de IA

---

## Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/demonevilperdiodpython/proyecto_sena.git
   cd proyecto_sena
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de entorno:**
   Copia el archivo `.env.example` a `.env` y configura tus valores locales:
   ```bash
   cp .env.example .env
   ```

5. **Aplicar migraciones:**
   ```bash
   cd project
   python manage.py migrate
   ```

6. **Ejecutar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
