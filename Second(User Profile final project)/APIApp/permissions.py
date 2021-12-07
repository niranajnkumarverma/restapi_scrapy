from rest_framework import permissions

class UpdateProfile(permissions.BasePermission):
    '''Allow user to edit their own profile'''

    def has_object_permission(self, request, view, obj):
        '''check whether user is trying to edit their own profile'''

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class UpdateTask(permissions.BasePermission):
    '''Allow user to update their tasks'''

    def has_object_permission(self, request, view, obj):
        '''check whether user is trying to update their own task'''

        if request.method in permissions.SAFE_METHODS:
            return True

        