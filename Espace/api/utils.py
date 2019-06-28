from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import User
from django.core.mail import EmailMultiAlternatives
from threading import Thread
import cloudinary
import os

class sendMailThread(Thread):
    def __init__(self, subject, body, email):
        self.subject = subject
        self.body = body
        self.email = email
        Thread.__init__(self)

    def run(self):
        text_content = "Welcome to NjokerioSacco"
        msg = EmailMultiAlternatives(
            self.subject,
            text_content,
            'kezzy.angiro@andela.com',
            ['kezzyangiro@gmail.com'])
        msg.attach_alternative(self.body, "text/html")
        msg.send()


#  Checking if user exists

forbidden = {'error': 'You are not authorised to perform this action'}


def getUser(self, pk):
    try:
        user = User.objects.get(id=pk)
        return user
    except Exception:
        raise ValidationError(
            detail={'error': 'User with that ID does not exist'})


def isAdmin(self, user):
    if not user.is_staff:
        raise PermissionDenied(forbidden)


def OwnerOrAdmin(self, user, pk):
    owner = User.objects.get(id=pk)
    a = owner != user
    b = not user.is_staff
    if a and b:
        raise PermissionDenied(forbidden)


def cloudinary_config():
    """ Cloudinary configuration settings """
    return cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )


def cloudinary_image_upload(one_file, image_name):
    """ Uploads an imaged to cloudinary """
    cloudinary_config()
    return cloudinary.uploader.upload(
        one_file,
        public_id=image_name,
        crop='limit',
        width='2000',
        height='2000',
        eager=[
            {'width': 200, 'height': 200,
             'crop': 'thumb', 'gravity ': 'auto',
             'radius': 20, 'effect': 'sepia'},
            {'width': 100, 'height': 150,
             'crop': 'fit', 'format ': 'png'}
        ],
        tags=['image_ad', 'NAPI']
    )
