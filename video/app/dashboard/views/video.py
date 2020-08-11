#coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect,reverse
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from app.model.video import VideoType,FromType,NationalityType,Video
from app.utils.common import check_and_get_video_type


class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self,request):

        error = request.GET.get('error','')
        data = {'error': error}

        videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['videos'] = videos

        return render_to_response(request,self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')

        if not all([name, image, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(reverse('external_video'), 'Error: missing important content'))

        result = check_and_get_video_type(
            VideoType, video_type, 'not proper video format')

        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))


        result = check_and_get_video_type(
            FromType, from_to, 'not a proper source')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result=['msg']))


        result = check_and_get_video_type(
            NationalityType, nationality,'not a proper nationality')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result=['msg']))

        Video.objects.create(
            name=name,
            image = image,
            video_type = video_type,
            from_to = from_to,
            nationality = nationality,
            info = info
        )

        return redirect(reverse('external_video'))

class VideoSub(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self,request,video_id):
        data = {}
        video = Video.objects.get(pk=video_id)

        data['video'] = video
        return render_to_response(request,self.TEMPLATE,data=data)

