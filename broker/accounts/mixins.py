from django.utils.http import urlsafe_base64_decode
from django.views import View

from accounts.models import Account


class TokenMixin(View):

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.user = None
        self.uid = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
            self.user = Account._default_manager.get(pk=self.uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            self.user = None
        return super().dispatch(request, *args, **kwargs)
