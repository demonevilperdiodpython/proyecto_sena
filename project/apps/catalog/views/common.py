from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from ..models import producto
from ..models import topics_group
from ..models import topic_section
from ..models import post as post_model
from ..forms import postForm
from ..forms import topic_groupForm
from apps.users.models import customuser as CustomUser
from ..models import postvideo
from ..models import postarchivo
# Helpers extraidos a utils para mantener views manejables.
from ..utils import (guardar_archivos, archivos_del_request, posts_del_feed,
                    sin_cuenta_no_se_puede_actuar, a_volver)
