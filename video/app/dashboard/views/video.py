#coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect,reverse
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from app.model.video import VideoType, FromType, NationalityType, Video, VideoSub,IdentityType,VideoStar
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

class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self,request,video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        error = request.GET.get('error','')

        data['video'] = video
        data['error'] = error
        return render_to_response(request,self.TEMPLATE,data=data)

    def post(self,request,video_id):
        url = request.POST.get('url')

        video = Video.objects.get(pk=video_id)

        length = video.video_sub.count()

        VideoSub.objects.create(video=video, url=url, number=length + 1)

        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))

class VideoStarView(View):

    def post(self,request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        path_format = ''.format(reverse('video_sub',kwargs={'video_id':video_id}))

        if not all([name,identity,video_id]):
            return redirect('{}?error={}'.format(path_format,'information is not complete'))

        IdentityType
        result = check_and_get_video_type(
            IdentityType, identity, 'illegal source')

        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path_format,result['msg']))
        video = Video.objects.get(pk=video_id)

        try:
            VideoStar.objects.create(
            video=video,
            name=name,
            identity=identity
        )
        except:
            return redirect('{}?error={}'.format(path_format,'Create file failed'))

        return redirect(reverse('video_sub',kwargs={'video_id': video_id}))

class StarDelete(View):

    def get(self, request, star_id,video_id):
        star = VideoStar.objects.filter(id=star_id).delete()

        return redirect(reverse('video_sub',kwargs={'video_id':video_id}))