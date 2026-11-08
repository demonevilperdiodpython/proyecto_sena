from .common import *
from .ai import (
    doc_como_argumento,
    _get_historial,
    _guardar_historial,
    _contexto_ia,
    group_contexto_ia,
    ia_view,
    ia_api_view,
    ia_response,
    
)
from .auth import (
    para_registrarse,
)
from .feed import (
    home,
    search_view,
    search_view_post,
    settings_view,
    popular,
)
from .posts import (
    eliminate_post,
    edit_post,
    post_detail,
    rate_post,
)
from .groups import (
    add_group,
    rate_group,
    subscribe,
    topic_group,
    edit_group,
    eliminate_group,
)
from .sections import (
    topic_section_view,
    post_in_section,
    add_section,
    edit_section,
    eliminate_section,
)
