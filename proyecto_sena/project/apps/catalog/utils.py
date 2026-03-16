def SepareByClass(set):
    categorias = {}
    Grup = set.objects.all()
    
    for i in Grup:
        categoria = i.categoria
        if categoria not in categorias:
            categorias[categoria] = [i]
        else:
            categorias[categoria].append(i)
    return categorias