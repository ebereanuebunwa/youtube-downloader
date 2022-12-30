from django.shortcuts import render, redirect
from django.views.generic import View
from pytube import YouTube
import os
# Create your views here.

class Home(View):
    def __init__(self, url=None):
        self.url = url

    def get(self, request):
        return render(request, 'app/index.html')

    def post(self, request):
        # For fetching the video
        if request.POST.get('fetch-vid'):
            self.url = request.POST.get('given_url')
            video = YouTube(self.url)
            vid_title, vid_thumbnail = video.title, video.thumbnail_url
            qual, stream = [], []
            for vid in video.streams.filter(progressive=True):
                qual.append(vid.resolution)
                stream.append(vid)
            context = {'vid_title': vid_title, 'vid_thumbnail': vid_thumbnail, 
                        'qual': qual, 'stream': stream,
                       'url': self.url} 
            return render(request, 'app/index.html', context)

        # For downloading the video
        elif request.POST.get('download-vid'):
            self.url = request.POST.get('given_url')
            video = YouTube(self.url)
            stream = [x for x in video.streams.filter(progressive=True)]
            chosen_qual = stream[int(request.POST.get('download-vid'))] 
            chosen_qual.download(output_path=f"{os.environ['UserProfile']}/Downloads")
            return redirect('home')

        return render(request, 'app/index.html')