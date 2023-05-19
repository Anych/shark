from django.contrib.sites import requests
from django.shortcuts import redirect

from accounts.models import UserProfile


def _profile(user):
    profile = UserProfile()
    profile.user_id = user.id
    profile.save()


def _redirect_to_next_page(request):

    url = request.META.get('HTTP_REFERER')
    query = requests.utils.urlparse(url).query
    params = dict(x.split('=') for x in query.split('&'))
    if 'next' in params:
        nextPage = params['next']
        return redirect(nextPage)
