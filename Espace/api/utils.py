from rest_framework.exceptions import ValidationError
from .models import User

#  Checking if user exists
def getUser(self, pk):
        try:
            user = User.objects.get(id=pk) 
            return user
        except Exception:
            raise ValidationError(detail={'error': 'User with that ID does not exist'})