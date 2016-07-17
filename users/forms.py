from registration.forms import RegistrationForm as BaseRForm
from models import User

class RegistrationForm(BaseRForm):
    class Meta(BaseRForm.Meta):
        model = User
        fields = (
            User.USERNAME_FIELD,
            'password1',
            'password2',
        )
        required_css_class = 'required'
