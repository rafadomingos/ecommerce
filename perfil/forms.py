from django import forms
from . import models
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Senha',
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Confirmação de Senha',
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'Email já existe'
        error_msg_email_exists = 'Email já existe'
        error_msg_password_match = 'Senhas diferentes'
        error_msg_password_short = 'A senha precisa ter ao menos 6 caracteres'
        error_msg_password_required = 'Esse campo é obrigatório'

        # Usuários logados: atualizacao
        if self.usuario:
            if usuario_data != usuario_db.username:
                if usuario_db:
                    validation_error_msgs['username'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

            if email_data != email_db.email:
                validation_error_msgs['email'] = error_msg_email_exists

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short

        # Usuários não logados: insert
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_email_exists

            if password_data != password2_data:
                validation_error_msgs['password'] = error_msg_email_exists
                validation_error_msgs['password2'] = error_msg_email_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_password_required

            if not password2_data:
                validation_error_msgs['password'] = error_msg_password_required

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))
