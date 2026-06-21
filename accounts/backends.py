from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOuUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Busca o usuário onde o email OU o username seja igual ao valor digitado
            user = UserModel.objects.get(Q(email__iexact=username) | Q(username__iexact=username))
        except UserModel.DoesNotExist:
            return None
        
        # Verifica se a senha está correta e se o usuário pode se autenticar
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
