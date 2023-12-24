# sourcery skip: use-fstring-for-concatenation
import contextlib
import os
import shutil

import unicodedata
import re

from pytube import Playlist, YouTube
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

forceQuit = False
r = sr.Recognizer()

# NOTE: Taken from https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def local_audio_transcribe(path):
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        r.recognize_sphinx(audio_listened, language="en-US", show_all=False)


# a function to recognize speech in the audio file
# so that we don't repeat ourselves in in other functions
def simple_audio_transcribe(path):
    with sr.AudioFile(path) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)
    return text


def transcribe_audio(path):
    # use the audio file as the audio source
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        text = r.recognize_google(audio_listened)
    return text


# TODO FIXME a function that splits the audio file into chunks on silence
# and applies speech recognition (mostly unused, should be fixed and tested)
def get_large_audio_transcription_on_silence(path):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(
        sound,
        # experiment with this value for your target audio file
        min_silence_len=1000,
        # adjust this per requirement
        silence_thresh=sound.dBFS - 14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", e)
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text
    # return the text for all chunks detected
    return whole_text


# INFO Cleanup the leftovers
def cleanup():
    with contextlib.suppress(FileNotFoundError):
        os.remove("audio.wav")
    with contextlib.suppress(FileNotFoundError):
        os.remove("video.mp4")
    with contextlib.suppress(FileNotFoundError):
        os.remove("audio.mp3")
    shutil.rmtree("audio-chunks")


# INFO Main youtube to mp4 downloader method
def download(link, target_filename="video"):
    url = YouTube(link)
    print("downloading....")
    video = url.streams.get_highest_resolution()
    print(video.title)
    path_to_download_folder = str(os.path.dirname(os.path.realpath(__file__)))  + "/downloads"
    video.download(path_to_download_folder, filename=target_filename + ".mp4")
    print("Downloaded! :)")
    return path_to_download_folder

# INFO Print a playlist info
def printPlaylist(playlist_link):
    playlist = Playlist(playlist_link)
    return playlist

# INFO Download a playlist
def managePlaylist(playlist, to_download=False, to_convert=False, named=True):
    print("Received playlist:", playlist)
    if not to_download:
        return playlist
    counter = 0
    path_to_download_folder = str(os.path.dirname(os.path.realpath(__file__))) + "/downloads"
    for url in playlist:
        counter += 1
        print("Downloading video", counter, "of", len(playlist))
        ytvideo = YouTube(url)
        video = ytvideo.streams.get_highest_resolution()
        filename = "video_" + str(counter)
        # Experimental name support
        if named:
            filename = slugify(ytvideo.title + "_" + ytvideo.author)
        print("Downloading : ", filename)
        video.download(path_to_download_folder, filename=filename + ".mp4")
        if to_convert:
            convert(path_to_download_folder, format="mp3", source_filename=filename, target_filename=filename)
    print("Downloaded all videos! :)")
    return path_to_download_folder

# INFO Get info about the video
def getInfo(link):
    print("Getting info for", link)
    url = YouTube(link)
    # Trying to sanitize the title
    title = url.title + "_" + url.author
    title = slugify(title)
    return {"title": url.title, "author": url.author, "length": str(url.length), "filename": title}


# INFO Convert the video to audio
def convert(path_to_download_folder, format="wav", source_filename="video", target_filename="audio"):
    src = f"{path_to_download_folder}/{source_filename}.mp4"
    dst = f"{path_to_download_folder}/{target_filename}.{format}"
    print("Converting to audio....")
    sound = AudioSegment.from_file(src, format="mp4")
    sound.export(dst, format=format)
    print("Converted to audio! :)")
    return dst


# Testing (at the moment it is testing with a random playlist)
if __name__ == "__main__":
    with contextlib.suppress(FileNotFoundError):
        cleanup()
        os.remove("transcription.txt")
    link = "https://www.youtube.com/playlist?list=PLXaw-xRbZ6E_LHJNJiIu-fOUo4SfpjHqE"
    playlist = printPlaylist(link)
    managePlaylist(playlist, to_download=True, to_convert=True)