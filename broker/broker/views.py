from django.shortcuts import render
from django.views import View


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'broker/index.html', {})


class PageNotFoundView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/404.html')


class PermissionDeniedView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/403.html')
