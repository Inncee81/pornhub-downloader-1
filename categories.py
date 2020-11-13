from urllib.request import urlopen
import re
import youtube_dl
import os
import html
import threading
import platform

if platform.system() == "Windows":
    separator = "\\"
else:
    separator = "/"

def download_video(url):
    os.system("youtube-dl -q " + url + " --format best")

def download_thread(urls, thread_count, thread_offset, path, category_name):
    print("Thread " + str(thread_offset) + " has been started")
    for i in range(thread_offset, len(urls), thread_count):
        url = "https://www.pornhub.com/view_video.php?viewkey=ph" + urls[i]
        download_video(url)
        print("Just downloaded video with url https://www.pornhub.com/view_video.php?viewkey=ph" + urls[i])

def get_categories():
    url = "https://www.pornhub.com/webmasters/categories"
    content = urlopen(url).read().decode("utf-8")
    return re.findall("\"id\":\"(\\d+)\",\"category\":\"(.*?)\"", content)

possible_categories = get_categories()

def search_category(category, video_count, path, thread_count, second_category = None, download = True):
    #The reason for the download being there is that during testing I don't want to have to wait 5 hours for downloads to happen.
    category_id = category[0]
    category_name = category[1]
    second_category_id = None
    second_category_name = None
    category_combined_name = category_name
    if second_category:
        second_category_id = second_category[0]
        second_category_name = second_category[1]
        if platform.system() == "Windows":
            category_combined_name += " "
        else:
            category_combined_name += "\\ "
        category_combined_name += second_category_name
        base_url = "https://pornhub.com/video/incategories/" + category_name + "/" + second_category_name
    else:
        base_url = "https://www.pornhub.com/video?c=" + category_id
    content = urlopen(base_url).read().decode("utf-8")
    video_pattern = "<a href=\"/view_video\\.php\\?viewkey=ph(.*?)\""
    videos = re.findall(video_pattern, content)
    
    os.system("mkdir " + path + separator + category_combined_name)

    links = []
    searchprefix = "https://www.pornhub.com/view_video.php?viewkey=ph"
    should_continue = True
    page_number = 1
    iterator = 0
    print("Getting download links")
    while should_continue:
        should_continue = False
        for video in videos:
            if video in links:
                continue
            if iterator >= video_count:
                break
            iterator += 1
            url = searchprefix + video
            content = urlopen(url).read().decode("utf-8")
            categories = re.findall("data-context-category='(.*?)'", content)[0] + "," + re.findall("data-context-tag='(.*?)'", content)[0]
            if not category_name.lower() in categories.lower() and ((not second_category) or second_category and second_category_name.lower() in categories.lower()):
                #if at least one category name isn't there. This is really long because the second category might not exist.
                iterator -= 1
                continue
            name = re.findall("name=\"description\" content=\"(.*?)\"", content)[0]
            name = name[6:name.find(" on Pornhub.com, the best hardcore porn site. Pornhub is home to the widest selection of free ")]
            links.append(video)
        else:
            should_continue = True
            page_number += 1
            url = base_url + str(page_number)
            content = urlopen(url).read().decode("utf-8")
            videos = re.findall(video_pattern, content)
    print("Finished getting download links")
    
    if download:
        print("Starting download")
        threads = []
        for i in range(0, thread_count):
            threads.append(threading.Thread(target=download_thread, args=(links, thread_count, i, path, category_name)))
            threads[-1].start()
        
        for thread in threads:
            thread.join()
            if platform.system() == "Windows":
                command = "move"
            else:
                command = "mv"
            os.system(command + " *.mp4 " + path + separator + category_combined_name)

        print("Finished download")
    print("Done")
