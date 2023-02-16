from rest_framework import permissions



class IsAdmin(permissions.IsAdminUser):
    pass