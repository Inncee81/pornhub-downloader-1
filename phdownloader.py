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
        if len(download_categories[x][0]) > 0:
            to_print += str(download_categories[x][0][0][1])
        for y in range(1, len(download_categories[x][0])):
            to_print += " combined with " + download_categories[x][0][y][1]
        for y in range(0, len(download_categories[x][1])):
            if len(download_categories[x][0]) > 0:
                to_print += " with "
            else:
                to_print += "Literally anything with "
            to_print += download_categories[x][1][y][1] + " excluded"
        to_print += ": " + str(download_categories[x][2]) + " videos set to download"
        print(to_print)

def get_category(message):
    print(message)
    category_index = input_number(0, len(possible_categories))
    return (possible_categories[category_index][0], possible_categories[category_index][1])

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
        print("a: <category count> <excluded category count>: Add a new category to download. Pornhub only allows 2 combined categories and 1 excluded category.")
        print("v: View categories to download.")
        print("r: Remove a category from the download list.")
        print("d: Downloads the videos")
        print("c: Change the directory to download videos to.")
        print("C: Shows the download path")
        print("t: Change the number of threads to use")
        print("T: Show the number of threads to use")
    
    while command.startswith("a"):
        if len(command.split()) != 3:
            print("Wrong amount of arguments, 3 required.")
            break
        arguments = command.split()[1:]
        invalid_args = False
        for x in range(0, len(arguments)):
            if not arguments[x].isnumeric() or int(arguments[x]) < 0:
                print("Invalid argument, only whole numbers are allowed.")
                invalid_args = True
            arguments[x] = int(arguments[x])
        if arguments[0] > 2:
            print("Pornhub only allows for 2 combined categories.")
            invalid_args = True
        if arguments[1] > 1:
            print("Pornhub only allows for 1 excluded category.")
            invalid_args = True
        if invalid_args:
            break

        for x in range(0, len(possible_categories)):
            print(str(x) + ": " + possible_categories[x][1])

        add_categories = []
        exclude_categories = []#This is an array for future-proofing
        for x in range(0, arguments[0]):
            add_categories.append(get_category("Pick a category to add."))
        for x in range(0, arguments[1]):
            exclude_categories.append(get_category("Pick a category to exclude."))
        print("How many videos do you want to download from that category?")
        videos = input_number(1, 1000000)#If you're downloading 1000000 porn videos what is wrong with you?
        download_categories.append((add_categories, exclude_categories, videos))
        break#This is terrible practice, but python doesn't let you break out of if statements.

    if command == "v":
        display_categories(False)

    if command == "r":
        display_categories(True)
        print("Choose a category to remove.")
        category = input_number(0, len(download_categories))
        del download_categories[category]
    
    if command == "d":
        for category in download_categories:
            search_category(category, download_path, thread_count)
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
