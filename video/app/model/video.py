#coding:utf-8

from enum import Enum
from django.db import models

class VideoType(Enum):
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    other = 'other'

VideoType.movie.label = 'Movie'
VideoType.cartoon.label = 'Animation'
VideoType.episode.label = 'TV Series'
VideoType.variety.label = 'Variety Show'
VideoType.other.label = 'Others'

class FromType(Enum):
    youku = 'youku'
    custom = 'custom'
FromType.youku.label ='Youku'
FromType.custom.label ='Custom'

class NationalityType(Enum):
    china = 'China'
    japan = 'Japan'
    korea = 'Korea'
    america = 'America'
    other = 'Other'

NationalityType.china.label = 'China'
NationalityType.japan.label = 'Japan'
NationalityType.korea.label = 'korea'
NationalityType.america.label = 'America'
NationalityType.other.label = 'Other'

class Video(models.Model):
    name = models.CharField(max_length=100,null=False)
    image = models.CharField(max_length=500,default='')
    video_type = models.CharField(max_length=50,default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True,db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return self.name

class VideoStar(models.Model):
    video = models.ForeignKey(
            Video,
            related_name='video_star',
            on_delete=models.SET_NULL,
            blank=True,null=True
    )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name

class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    url = models.CharField(max_length=500,null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{}, number:{}'.format(self.video.name,self.number)



