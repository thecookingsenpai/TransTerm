# sourcery skip: use-fstring-for-concatenation
import speech_recognition as sr
from pytube import YouTube
import os
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil
import contextlib

forceQuit = False
r = sr.Recognizer()


def local_audio_transcribe(path):
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        text = r.recognize_sphinx(audio_listened, 
                                  language="en-US", 
                                  show_all=False)

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

# a function that splits the audio file into chunks on silence
# and applies speech recognition


def get_large_audio_transcription_on_silence(path):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=1000,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS-14,
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

def cleanup():
	with contextlib.suppress(FileNotFoundError):
		os.remove("audio.wav")
	with contextlib.suppress(FileNotFoundError):
		os.remove("video.mp4")
	with contextlib.suppress(FileNotFoundError):
		os.remove("audio.mp3")
	shutil.rmtree("audio-chunks")

def download(link):
	url = YouTube(link)
	print("downloading....")
	video = url.streams.get_highest_resolution()
	print(video.title)
	path_to_download_folder = str(os.path.dirname(os.path.realpath(__file__)))
	video.download(path_to_download_folder, filename="video.mp4")
	print("Downloaded! :)")
	return path_to_download_folder

def getInfo(link):
    print("Getting info for", link)
    url = YouTube(link)
    return {
        "title": url.title,
        "author": url.author,
        "length": str(url.length)
    }

def convert(path_to_download_folder, format="wav"):
    src = f"{path_to_download_folder}/video.mp4"
    dst = f"{path_to_download_folder}/audio.{format}"
    print("Converting to audio....")
    sound = AudioSegment.from_file(src, format="mp4")
    sound.export(dst, format=format)
    print("Converted to audio! :)")
    return dst

# Standalone support
if __name__ == "__main__":
	with contextlib.suppress(FileNotFoundError):
		cleanup()
		os.remove("transcription.txt")
	link = "https://www.youtube.com/watch?v=b1ukaC9cSKQ"
    # download the video
	folder = download(link)
 	# convert the video to audi
    # Optionally, you can transcribe the audio to text
	choice = input("Do you want to transcribe the audio? (y/n)")
	if choice != "y":
		print("Skipping transcription...")
		convert(folder, format="mp3")
		print("Transcription skipped! Video and audio (in mp4 and mp3 format) are here!")
		exit()
    # We need a wav file for the transcription
	dst = convert(folder)
    # Convert the audio to text
	print("Converting audio to text...")
	type_of_transcription = 0
	while type_of_transcription not in ["1", "2", "3"]:
		print("Select 1, 2 or 3")
		print("Do you prefer to transcribe the audio:\n" + 
        	  "1) With the normal transcriber (best on short videos)\n" + 
              "2) With the transcriber that split silences (best on long videos but may be inaccurate)\n" + 
              "3) Using Sphynx CMU (uses your computer to transcribe the audio)")
		type_of_transcription = input()
		if type_of_transcription not in ["1", "2", "3"]:
			print("Please select 1, 2 or 3")
	print("Transcribing audio...be patient, this may take a while...")
	if type_of_transcription == "1":
		txt = simple_audio_transcribe(dst)
	elif type_of_transcription == "2":
		txt = get_large_audio_transcription_on_silence(dst)
	elif type_of_transcription == "3":
		txt = local_audio_transcribe(dst)
    # print the transcription
	print(txt)
    # Save the transcription
	with open("transcription.txt", "w") as f:
		f.write(txt)
  	# cleanup
	with contextlib.suppress(FileNotFoundError):
		cleanup()
