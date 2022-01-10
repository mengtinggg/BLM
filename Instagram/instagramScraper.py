from instaloader import Instaloader

L = Instaloader(download_pictures = False, download_videos=False, download_video_thumbnails = False, save_metadata = False, download_comments = True)

hashtag_list = ['blacklivesmatter']

for element in hashtag_list:
    L.download_hashtag(element, max_count = 100000, profile_pic = False)

