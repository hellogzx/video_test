#coding:utf-8

from django.views.generic import View
from app.libs.base_render import render_to_response
from django.shortcuts import redirect


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self,request):

        return render_to_response(request,self.TEMPLATE)

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username,password)
        return redirect('/dashboard/login')
