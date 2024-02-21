from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешаются запросы все, если он безопасные.
    И все запросы для администратора и суперадминистратора.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin
                    or request.user.is_superuser)
                    )
                )


class IsAdmin(permissions.BasePermission):
    """
    Запросы разрешаться только администраторам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )

        def has_object_permission(self, request, view, obj):
            return (
                request.user.is_admin
                or request.user.is_superuser
            )


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Запросы разрешаться всем, если они безопасные.
    Изменения доступны только владельцу, администратору и модератору.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsOwner(permissions.BasePermission):
    """
    Доступ разрешен только владельцу.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated
