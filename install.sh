#!/bin/bash

pip3 install -r requirements.txt
#pip3 install -r requirements.txt --break-system-packages

echo "Preparing to install PortAudio for Python"

unameOut="$(uname -s)"
case "${unameOut}" in
Linux*) machine=Linux ;;
Darwin*) machine=Mac ;;
CYGWIN*) machine=Cygwin ;;
MINGW*) machine=MinGw ;;
*) machine="UNKNOWN:${unameOut}" ;;
esac

if [[ ${machine} == "Mac" ]]; then
	# check if homebrew is installed on Macos if not install Homebrew
	echo "Checking Homebrew"
	command -v brew >/dev/null 2>&1 || {
		echo >&2 "Installing Homebrew Now"
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	}
	# if homebrew is installed, update to latest
	brew update-reset
	# install portaudio
	brew install portaudio
	pip3 install pyaudio
elif [[ "$(expr substr $(uname -s) 1 5)" == "Linux" ]]; then
	sudo apt-get install -y portaudio19-dev
	sudo apt-get install python3-pyaudio
fi
