#coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect,reverse
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from app.model.video import VideoType, FromType, NationalityType, Video, VideoSub,IdentityType,VideoStar
from app.utils.common import check_and_get_video_type, handle_video


class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self,request):

        error = request.GET.get('error','')
        data = {'error': error}

        cus_videos = Video.objects.filter(from_to=FromType.custom.value)
        ex_videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['ex_videos'] = ex_videos
        data['cus_videos'] = cus_videos


        return render_to_response(request,self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')
        video_id = request.POST.get('video_id')
        if video_id:
            reverse_path = reverse('video_update',kwargs={'video_id': video_id})

        else:
            reverse_path = reverse('external_video')

        if not all([name, image, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(reverse_path, 'Error: missing important content'))

        result = check_and_get_video_type(
            VideoType, video_type, 'not proper video format')

        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result['msg']))


        result = check_and_get_video_type(
            FromType, from_to, 'not a proper source')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result=['msg']))


        result = check_and_get_video_type(
            NationalityType, nationality,'not a proper nationality')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result=['msg']))

        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image = image,
                    video_type = video_type,
                    from_to = from_to,
                    nationality = nationality,
                    info = info
                )
            except:
                return redirect('{}?error={}'.format(reverse_path, 'Create failed'))
        else:
            try:
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.image = image
                video.video_type = video_type
                video.from_to = from_to
                video.nationality = nationality
                video.info = info
                video.save()
            except:
                return redirect('{}?error={}'.format(reverse_path,'change was failed'))
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
        number = request.POST.get('number')
        videosub_id = request.POST.get('videosub_id')

        video = Video.objects.get(pk=video_id)

        if FromType(video.from_to) == FromType.custom:
            url = request.FILES.get('url')
        else:
            url = request.POST.get('url')

        url_format = reverse('video_sub', kwargs={'video_id': video_id})

        if not all([url,number]):
            return redirect('{}?error={}'.format(url_format,'information is not complete'))

        if FromType(video.from_to) == FromType.custom:
            handle_video(url, video_id, number)
            return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

        if not videosub_id:
            try:
                VideoSub.objects.create(video=video, url=url, number=number)
            except:
                return redirect('{}?error={}'.format(url_format, 'failed to create new data'))

        else:
            video_sub = VideoSub.objects.get(pk=videosub_id)
            try:
                video_sub.url = url
                video_sub.number = number
                video_sub.save()
            except:
                return redirect('{}?error={}'.format(url_format, 'change failed'))
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

class VideoStarView(View):

    def post(self,request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        video = Video.objects.get(pk=video_id)

        if FromType(video.from_to) == FromType.custom:
            url = request.Files.get('url')
        else:
            url = request.POST.get('url')

        path_format = ''.format(reverse('video_sub',kwargs={'video_id':video_id}))

        if not all([name,identity,video_id]):
            return redirect('{}?error={}'.format(path_format,'information is not complete'))

        IdentityType
        result = check_and_get_video_type(
            IdentityType, identity, 'illegal source')

        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path_format,result['msg']))


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

class SubDelete(View):

    def get(self,request,videosub_id,video_id):
        VideoSub.objects.filter(id=videosub_id).delete()

        return redirect(reverse('video_sub', kwargs = {'video_id': video_id}))

class VideoUpdate(View):
    TEMPLATE = 'dashboard/video/video_update.html'

    @dashboard_auth
    def get(self,request,video_id):
        data = {}
        video = Video.objects.get(pk=video_id)

        data['video'] = video
        return render_to_response(request,self.TEMPLATE,data=data)

class VideoUpdateStatus(View):

    def get(self,request,video_id):

        video = Video.objects.get(pk=video_id)
        video.status = not video.status
        video.save()

        return redirect(reverse('external_video'))