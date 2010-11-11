# -*- coding: utf-8 -
#
# This file is part of dj-webmachine released under the MIT license. 
# See the NOTICE for more information.

import binascii

from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from webmachine.exc import HTTPClientError

class Auth(object):

    def authorized(self, request):
        return True

class BasicAuth(Auth):

    def __init__(self, func=authenticate, realm="API"):
        self.func = func
        self.realm = realm

    def authorized(self, req, resp):
        auth_str = req.META.get("HTTP_AUTHORIZATION")
        if not auth_str:
            return False

        try:
            (meth, auth) = auth_str.split(" ", 1)
            if meth.lower() != "basic":
                # bad method
                return False
            auth1 = auth.strip().decode('base64')
            (user, pwd) = auth1.split(":", 1)
        except (ValueError, binascii.Error):
            raise HTTPClientError()

        req.user = self.func(username=user, password=pwd)
        if not req.user:
            req.user = AnonymousUser()
            return 'Basic realm="%s"' % self.realm
        return True

