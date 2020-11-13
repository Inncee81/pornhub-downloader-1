from urllib.request import urlopen
import re
import youtube_dl
import os
import html
import threading
import platform

separator = "/"
space_separator = "\\ "

def download_video(url):
    os.system("youtube-dl -q " + url + " --format best")

def download_thread(urls, thread_count, thread_offset, path):
    print("Thread " + str(thread_offset) + " has been started")
    for i in range(thread_offset, len(urls), thread_count):
        url = "https://www.pornhub.com/view_video.php?viewkey=ph" + urls[i]
        download_video(url)
        print("Just downloaded video with url https://www.pornhub.com/view_video.php?viewkey=ph" + urls[i])

def run_command(command, inputs):
    bad_os = platform.system() == "Windows"
    if command == "mkdir":
        if bad_os:
            os.system("mkdir \"" + inputs[0].replace("/", "\\").replace("\\ ", " ") + "\"")
            #C:/Windows/System\ 32 -> "C:\Windows\System 32"
            #/ is an illegal character for windows filenames, and this relies on that fact.
        else:
            os.system("mkdir " + inputs[0])

    if command == "mv":
        if bad_os:
            os.system("move \"" + inputs[0].replace("/", "\\").replace("\\ ", " ") + "\" \"" + inputs[1].replace("/", "\\").replace("\\ ", " ") + "\"")
            #Convert paths to directories and move the file between.
        else:
            os.system("mv " + inputs[0] + " " + inputs[1])
            #Do it normally because linux is perfect and OS X is not a dumpster fire.

def get_categories():
    url = "https://www.pornhub.com/webmasters/categories"
    content = urlopen(url).read().decode("utf-8")
    return re.findall("\"id\":\"(\\d+)\",\"category\":\"(.*?)\"", content)

possible_categories = get_categories()

def search_category(category, path, thread_count, download = True):
    #The reason for the download being there is that during testing I don't want to have to wait 5 hours for downloads to happen.
    if platform.system() == "Windows":
        path = path.replace("\\", "/")
        #I want to parse linux commands into windows commands, and in order to do that I have to first generate linux commands with this. I hate windows.
    video_count = category[2]

    include_category_ids = []
    include_category_names = []
    for include in category[0]:
        include_category_ids.append(include[0])
        include_category_names.append(include[1])

    exclude_category_ids = []
    exclude_category_names = []
    for exclude in category[1]:
        exclude_category_ids.append(exclude[0])
        exclude_category_names.append(exclude[1])

    category_combined_name = ""
    if len(include_category_names) >= 1:
        category_combined_name += "include" + space_separator
        for name in include_category_names:
            category_combined_name += name + space_separator

    if len(exclude_category_names) >= 1:
        category_combined_name += "exclude" + space_separator
        for name in exclude_category_names:
            category_combined_name += name + space_separator

    if len(category[0]) > 1:
        base_url = "https://pornhub.com/video/incategories"
        for name in include_category_names:
            base_url += "/" + name
    elif len(category[0]) == 1:
        base_url = "https://www.pornhub.com/video?c=" + include_category_ids[0]
    else:
        base_url = "https://www.pornhub.com"
    if len(exclude_category_names) > 0:
        base_url += "?o=mr&exclude_category=" + exclude_category_ids[0]
        #I know this is an array for future proofing, but there is no precedent for how this would be done.
    content = urlopen(base_url).read().decode("utf-8")
    video_pattern = "<a href=\"/view_video\\.php\\?viewkey=ph(.*?)\""
    videos = re.findall(video_pattern, content)

    print(path + "/" + category_combined_name)
    run_command("mkdir", (path + "/" + category_combined_name))

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
            passed = True
            for include in include_category_names:
                if not include.lower() in categories.lower():
                    passed = False
                    break
            for exclude in exclude_category_names:
                if exclude.lower() in categories.lower():
                    passed = False
                    break
            if not passed:
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
            threads.append(threading.Thread(target=download_thread, args=(links, thread_count, i, path)))
            threads[-1].start()
        
        for thread in threads:
            thread.join()
        run_command("mv", ("*.mp4", path + separator + category_combined_name))

        print("Finished download")
    print("Done")
