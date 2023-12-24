# TransTerm

A terminal based YouTube video and playlist downloader (mp4, mp3, wav) and transcriber with a nice TUI interface.


![transterm](https://i.imgur.com/woRKbiK.png)

PS. The transparency and retro term is proper of my KDE Plasma configuration

🌲🌲🌲🦌🌲🌲🌲🦌🌲🌲🌲

**By utilizing TransTerm, you acknowledge that you have read, comprehended, and agreed to the terms set forth in the disclaimer at the bottom of this file.**

# Table of Contents
1. [What is TransTerm?](#what-is-this)
2. [Features](#features)
3. [Installation](#installation)
    - [For Mac & Linux](#installation-for-mac--linux)
    - [Troubleshooting](#troubleshooting)
    - [For Windows](#installation-for-windows)
4. [Usage](#usage)
5. [Manual Mode (Debug)](#manual-mode-aka-debug)
6. [Contributing](#contributing)
7. [License](#license)
8. [Disclaimer](#disclaimer)
    - [Terms and Conditions](#terms-and-conditions)
        - [Appropriate Use](#appropriate-use)
            - [Copyright Adherence](#copyright-adherence)
            - [Personal Usage](#personal-usage)
            - [Third-Party Content](#third-party-content)
        - [Limitation of Responsibility](#limitation-of-responsibility)


## What is this

TransTerm is an highly experimental text based graphical user interface to act on YouTube videos.

Being text based, this program runs even in the terminal.

## Features

- Download any youtube video at the highest resolution by default in mp4 format
- Is able to automatically convert the downloaded video both in mp3 or wav format
- Playlist support for the above features including automatically rename the files using the video title and the channel name
- Transcribe a ssingle downloaded video using either:
  • Google Audio to Text
  • Google Audio to Text + Silence detection
  • Sphynx CMU (processed offline locally)

## Installation for Mac & Linux

      git clone https://github.com/thecookingsenpai/transterm && cd transterm

      sudo chmod +x install.sh

      ./install.sh

## Troubleshooting

In some cases, where python3 environment is managed by the system and not by pip3, it is advisable to install the dependencies manually as you would do with your system. If you want to force the installation anyway, first run:

      pip3 install -r requirements.txt --break-system-packages

The same general solution applies to any requirements problem. PLease note that using the above command is not recommended as it could break your python installation.

## Installation for Window

      git clone https://github.com/thecookingsenpai/transterm && cd transterm && pip3 install -r requirements.txt

## Usage

      python3 gui.py

## Manual mode (aka debug)

You can edit the bottom part of term.py so that after the

      if __name__ == "__main__":

condition you can write your own logic. Then, launch with:

      python3 term.py

For convenience, a playlist example is already included (with the best playlist ever, I'd say).

## Contributing

You are welcome and free to contribute to the project. To do that, you have a few ways:

- Add some kind of functionality and create a PR
- Search the lines marked with TODO and FIXME in the code for the most urgent things
- In any case, thank you!

## License

CreativeCommons BY-NC-SA 4.0

## Disclaimer

### Terms and Conditions:

TransTerm is a YouTube downloader and transcriber application developed for personal, non-commercial use. Users must ensure that their utilization of this tool complies with all relevant laws and regulations in their jurisdiction.

### Appropriate Use:

#### Copyright Adherence:

Users must respect the copyrights and intellectual property rights of content creators. TransTerm should not be utilized to infringe upon copyrights or distribute content without proper authorization.

#### Personal Usage:

The application is intended for personal use, allowing users to download and transcribe YouTube videos for lawful purposes such as education, research, or similar activities. Commercial use or distribution of downloaded/transcribed content without authorization is strictly prohibited.

#### Third-Party Content:

Users are responsible for confirming that they possess the legal rights to download and transcribe any third-party content from YouTube. TransTerm does not endorse or encourage the unauthorized downloading or distribution of copyrighted materials.

### Limitation of Responsibility:

The developers of TransTerm are not accountable for any misuse or illegal use of the tool. Users accept all associated risks with their use of the application and agree to comply with applicable laws and YouTube's terms of service.

***Please Note: This disclaimer does not serve as legal advice. Users are encouraged to seek legal counsel if they have queries regarding the legality of their use of TransTerm in their specific jurisdiction.***

**By utilizing TransTerm, you acknowledge that you have read, comprehended, and agreed to the terms set forth in this disclaimer.**
