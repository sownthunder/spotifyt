![intro](http://i.imgur.com/pb1sEG6.gif)

# Spotifyt 0.7.01
#### *Download songs from your Spotify playlists*

> **Spotifyt** will search and download all the songs in a Spotify playlist in MP3 format with Album covers. It's fast and really easy to use.

# How does it work ?
Given a playlist, Spotifyt gets the name from all of the songs in your list, to seach and download all of them from Youtube. 

# How to download and install Spotifyt ?
### 1. Clone the repository
`git clone https://github.com/luastan/spotifyt.git`
### 2. cd into the cloned repository and run the setup utility (you might need to be a super user for this)
`cd spotifyt`
`sudo python3 setup.py install`
### 3. Install FFMPEG with your favourite package manager
**Debian/Ubuntu:** `sudo apt-get install ffmpeg`
**Arch Linux:** `sudo pacman -Ss ffmpeg`
**Fedora/Suse/RedHat...:** `sudo yum install ffmpeg`

# Usage:
**Print help with:** `python3 -m spotifyt -h`

**Usage output:**
´usage: spotifyt [-h] [-d [DIRECTORY]] [-k] [--version]
                [PLAYLIST [PLAYLIST ...]]

Song download automation via CLI by @luastan

positional arguments:
  PLAYLIST        Spotify's playlist URL/URI to download

optional arguments:
  -h, --help      show this help message and exit
  -d [DIRECTORY]  Download Directory
  -k              Delete saved API keys
  --version       show program's version number and exit
´

# FAQ
#### Does it require extra software to work ?
Requires FFMPEG

# !
I'm not ressponsible for the use of Spotifyt. I made it as a fun project to learn python, and I personally don't use it. Downloading videos from youtube violates their terms of service. Using Spotifyt to download mostly copyrighted material in bulk is ilegal. 

# License

Released under the [GNU GPL v3](LICENSE).
