#Pornhub category downloader
This runs on python so you'll have to download that.

Please note that all the testing so far has been done in linux, so there's a pretty good chance that this will break on windows, although it shouldn't.

To use this, you need to install something called youtube-dl. If you don't have this, the program will not work. Yes, it was made to download youtube videos but it also works on pornhub for some reason.

If you have pip, it can be installed with pip3 install youtube-dl


Please set the thread count to a factor of the downloaded video count. I don't know why this breaks the program, and it might work on Windows, but it doesn't work on Linux. When I say downloaded video count, I mean for each category individually. If you're running 4 threads, having 6 downloads in one category and 6 downloads in another won't work.

Also, every once in a while this program will download a video which isn't in the specified categories, I don't know why that happens.
