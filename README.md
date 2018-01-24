![intro](http://i.imgur.com/pb1sEG6.gif)

# Spotifyt 0.7.01
#### *Download songs from your Spotify playlists*

> **Spotifyt** will search and download all the songs in a Spotify playlist in MP3 format with Album covers. It's fast and really easy to use. Also, Spotifyt is not resource heavy so, you can leave it running in the background while you do other stuff. 

# How to download and install Spotifyt ?
Download the latest portable release for windows (x64 bit) from the [releases page](https://github.com/luastan/spotifyt/releases). This executable file is portable so you just have to download and run it.



# How to use ?
Spotifyt is really easy to use:

1. Launch Spotifyt.
2. Copy the desired playlist link. (You can find it as options to share your playlist)
3. Cick Download ! (Spotifyt will grab the link you copied).
4. Choose a Folder(Directory) to store your songs.
5. Wait for the download to finish and enjoy ;) .




### How does it work ?
Given a playlist, Spotifyt gets the name from all of the songs in your list, to seach and download all of them from Youtube. 

Spotifyt is very efficient. If It finds out that a song has already been fully downloaded, it won't wonload it again, so if you stop the program before finishing downloading, next time you try to download the same playlist, Spotifyt will continue where it stopped.

Whenever an update is available, Spotifyt will get u to know by showing a message before starting the program. I highly suggest to download the newer versions, because they migth fix bugs that prevent songs from being downloaded propperly.





# FAQ
#### Does it work in Linux, Mac Os.... ?
You should be able to run the code in every Unix based OS(such as linux), windows or mac. The portable version is only available for windows tho. I'm pretty sure you can make it run on some python environments for Android and iOS without so much effort.

#### Does it require extra software to work ?
The portable version requires nothing but an updated win vista/7/8/8.1/10 system. To run the code directly use pip to install the required libraries `python3 -m pip install -r requirements.txt`. ffmpeg is needed too. Also the code is not gonna work unless you place your Spotify developer credentials [here](https://github.com/luastan/spotifyt/blob/master/spotifyt/__main__.py#L68). Get your credentials in the [Spotify Developer webpage](https://developer.spotify.com/)



#### Does it have malicious code ?
No. It also has no privative code so you can read it all and make your own conclusions lol. I didn't sign the binaries tho, cuz im lazy =).



# !
I'm not ressponsible for the use of Spotifyt. I made it as a fun project to learn python, and I personally don't use it. Downloading videos from youtube violates their terms of service. Using Spotifyt to download mostly copyrighted material in bulk is ilegal. 

# License

Released under the [GNU GPL v3](LICENSE).
