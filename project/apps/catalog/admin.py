from django.contrib import admin
from .models import producto, topics_group, topic_section, post, postimagen, postvideo

class PostImagenInline(admin.TabularInline):
    model = postimagen
    extra = 1

class PostVideoInline(admin.TabularInline):
    model = postvideo
    extra = 1

@admin.register(post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'parent', 'created_at', 'content_snippet')
    list_filter = ('created_at', 'group')
    search_fields = ('content', 'user__username', 'group__nombre')
    inlines = [PostImagenInline, PostVideoInline]

    def content_snippet(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_snippet.short_description = 'Contenido'

@admin.register(topics_group)
class TopicsGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'score')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)

@admin.register(topic_section)
class TopicSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    search_fields = ('name', 'group__nombre')
    list_filter = ('group',)

@admin.register(producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)

@admin.register(postimagen)
class PostImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'tittle')

@admin.register(postvideo)
class PostVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'tittle')
