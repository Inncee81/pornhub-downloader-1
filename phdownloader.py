from categories import *

download_categories = []
if platform.system() == "Windows":
    download_path = "downloaded videos"
else:
    download_path = "downloaded\\ videos"
thread_count = 4

def display_categories(should_number):
    for x in range(0, len(download_categories)):
        to_print = ""
        if should_number:
            to_print = "(" + str(x) + ") "
        to_print += str(download_categories[x][0][1])
        if len(download_categories[x]) == 3:
            to_print += " combined with " + download_categories[x][2][1]
        to_print += ": " + str(download_categories[x][1]) + " videos set to download"
        print(to_print)

def input_number(smallest, largest):
    i = input()
    while not (i.isnumeric() and smallest <= int(i) < largest):
        print("That's not a valid option.")
        i = input()
    return int(i)

while True:
    print("Enter in the next command (Type \"help\" for help)")
    command = input()
    if command == "help":
        print("a: Add a new category to the list of categories to download.")
        print("ac: Add a combined category")
        print("v: View categories to download.")
        print("r: Remove a category from the download list.")
        print("d: Downloads the videos")
        print("c: Change the directory to download videos to.")
        print("C: Shows the download path")
        print("t: Change the number of threads to use")
        print("T: Show the number of threads to use")
    
    if command == "a":
        for x in range(0, len(possible_categories)):
            print(str(x) + ": " + possible_categories[x][1])

        print("Pick a category to add.")
        category_index = input_number(0, len(possible_categories))
        category = (possible_categories[category_index][0], possible_categories[category_index][1])
        print("How many videos do you want to download from that category?")
        videos = input_number(1, 1000000)#If you're downloading 1000000 porn videos what is wrong with you?
        download_categories.append((category, videos))
    
    if command == "ac":
        for x in range(0, len(possible_categories)):
            print(str(x) + ": " + possible_categories[x][1])

        print("Pick a category to add.")
        first_category_index = input_number(0, len(possible_categories))
        print("Pick a second category to add.")
        second_category_index = input_number(0, len(possible_categories))
        first_category = (possible_categories[first_category_index][0], possible_categories[first_category_index][1])
        second_category = (possible_categories[second_category_index][0], possible_categories[second_category_index][1])
        print("How many videos do you want to download from that category?")
        videos = input_number(1, 1000000)#If you're downloading 1000000 porn videos what is wrong with you?
        download_categories.append((first_category, videos, second_category))

    if command == "v":
        display_categories(False)

    if command == "r":
        display_categories(True)
        print("Choose a category to remove.")
        category = input_number(0, len(download_categories))
        del download_categories[category]
    
    if command == "d":
        for category in download_categories:
            if len(category) == 2:
                search_category(category[0], category[1], download_path, thread_count)
            else:
                search_category(category[0], category[1], download_path, thread_count, second_category = category[2])
        break

    if command == "c":
        print("Please enter in the new download path")
        download_path = input()
    
    if command == "C":
        print("Download path: " + download_path)

    if command == "t":
        print("Please enter in the new thread count")
        thread_count = input_number(1, 1000000)
    
    if command == "T":
        print("Thread count: " + str(thread_count))
