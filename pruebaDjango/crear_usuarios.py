
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.denuncia.models import Denuncia

consulta_group, _ = Group.objects.get_or_create(name='consulta')
editor_group, _ = Group.objects.get_or_create(name='editor')

consulta = User.objects.create_user('consulta', password='1234')
editor = User.objects.create_user('editor', password='1234')
admin = User.objects.create_superuser('admin', email='admin@example.com', password='1234')

consulta.groups.add(consulta_group)
editor.groups.add(editor_group)

ct = ContentType.objects.get_for_model(Denuncia)
edit_permissions = Permission.objects.filter(content_type=ct, codename__startswith='change')
editor_group.permissions.set(edit_permissions)

view_permissions = Permission.objects.filter(content_type=ct, codename__startswith='view')
consulta_group.permissions.set(view_permissions)

print("Usuarios y roles creados correctamente.")
