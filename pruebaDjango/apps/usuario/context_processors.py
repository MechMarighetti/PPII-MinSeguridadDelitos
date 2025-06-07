def roles_context(request):
    if request.user.is_authenticated:
        grupos = request.user.groups.values_list('name', flat=True)
        return {
            'is_admin': request.user.is_superuser,
            'is_editor': 'editor' in grupos,
            'is_consulta': 'consulta' in grupos,
        }
    return {}
