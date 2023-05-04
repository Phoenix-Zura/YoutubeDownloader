import pytube

def video_downloader():

    vid_url=str(input("Enter Video URL: "))
    print('Connecting, Please wait...')
    video=pytube.YouTube(vid_url)
    Streams=video.streams
    File_name=input('File Name:')
    Format=input('Audio Or Video :')

    if Format=='Audio':
        Filter=Streams.get_audio_only(subtype='mp4')
    if Format=='Video':
        Filter=Streams.get_highest_resolution()
    print('Now downloading:',video.title)
    sizer=round(Filter.filesize/1000000)
    print('Size:',sizer,'MB')


    Filter.download(filename=str(File_name))
    print('Done!')
video_downloader()

