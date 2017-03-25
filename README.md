![intro](http://i.imgur.com/pb1sEG6.gif)

# Spotifyt 0.5
#### *Download songs from your Spotify playlists*

> **Spotifyt** will search and download all the songs in a Spotify playlist in MP3 format with Album covers and other Metadata. It's fast and really easy to use. Also, Spotifyt is not resource heavy so, you can leave it running in the background while you do other stuff. 


### How does it work ?
Given a playlist, Spotifyt gets the name from all of the songs in your list, to search every single one in youtube and download it from [YoutubeInMp3](https://www.youtubeinmp3.com/). This means you should keep in mind YoutubeInMp3's [Terms of Service](https://www.youtubeinmp3.com/tos/) while using my program. 


# How to use ?
Spotifyt is really easy to use:

1. Launch Spotifyt.
2. Copy the desired playlist link. It supports either the URI or the open.spotify direct link. (You can find them as options to share your playlist)
3. Cick Download ! (Spotifyt will grab the link you copied).
4. Choose a Folder(Directory) to store your songs.
5. Wait for the download to finish and enjoy ;) .


# How to download and install Spotifyt ?
You can clone the repository and run the code directly or download the latest portable release for windows (x64 bit) from the [releases page](https://github.com/luastan/spotifyt/releases). This executable file is portable so you just have to download and run it.


# FAQ
#### Does it work in Linux, Mac Os.... ?
You should be able to run the code in every Unix based OS(such as linux), windows or mac. The portable version is only available for windows tho. I'm pretty sure you can make it run on some python environments for Android and iOS without so much effort.

#### Does it require extra software to work ?
The portable version requires nothing but an updated win vista/7/8/8.1/10 system. To run the code use pip to install the required libraries: `pip install -r requirements.txt`

#### Why it didn't download all my playlist songs? 
There's a small chance where Spotifyt won't be able to retrieve MP3 files from YoutubeInMp3, in those cases the program will retry downloading the file a few times. After 10 failed attempts to download a song, It will be skipped and at the end of the downloads you will be asked if you want to save a file with the links Spotifyt was unable to download.

#### Is it legal ?
By respecting YoutubeInMp3's [Terms of Service](https://www.youtubeinmp3.com/tos/) while using Spotifyt, you should be good.

#### Does it have malicious code ?
No. Also it has no privative code so you can read it all and make your own conclusions lol.


# License

Released under the [GNU GPL v3](LICENSE).
