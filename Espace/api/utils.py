from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import User

#  Checking if user exists

forbidden = {'error':'You are not authorised to perform this action'}

def getUser(self, pk):
        try:
            user = User.objects.get(id=pk) 
            return user
        except Exception:
            raise ValidationError(detail={'error': 'User with that ID does not exist'})

def isAdmin(self, user):
    if not user.is_staff:
            raise PermissionDenied(forbidden) 

def OwnerOrAdmin(self, user, pk):
    owner = User.objects.get(id=pk)
    a = owner != user
    b = not user.is_staff
    if a and b:
            raise PermissionDenied(forbidden) 
