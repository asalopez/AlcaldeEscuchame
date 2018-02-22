from django.core.exceptions import PermissionDenied
from usuarios.models import Ciudadano, Funcionario

def usuario_role_ciudadano(function):
    """Decorador que verifica que el usuario es de tipo ciudadano"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'ciudadano'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def usuario_role_funcionario(function):
    """Decorador que verifica que el usuario es de tipo funcionario"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'funcionario'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def usuario_role_administrador(function):
    """Decorador que verifica que el usuario es de tipo Administrador (y staff)"""

    def wrap(request, *args, **kwargs):
        if (hasattr(request.user.actor, 'administrador') and (request.user.is_staff)):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap