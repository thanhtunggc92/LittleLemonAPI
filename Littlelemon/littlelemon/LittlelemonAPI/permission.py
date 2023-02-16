from rest_framework import permissions



class IsManager(permissions.BasePermission):
    "check request.user is in manager group or not"


    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name='manager').exists())




class IsDeliveryCrew(permissions.BasePermission):
    "allow delivery crew to access"

    def has_permission(self, request, view):
        return bool (request.user.groups.filter(name='delivery_crew').exists())

   