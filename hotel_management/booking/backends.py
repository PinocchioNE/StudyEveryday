# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, id_card=None, phone_number=None,  **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(id_card=id_card, phone_number=phone_number)

            return user
        except UserModel.DoesNotExist:
            return None
