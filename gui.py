import random
import threading
from statistics import mean

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    RichLog,
    Select,
    Sparkline,
)

import term


class TransTerm(App):
    CSS_PATH = "meshterm.tcss"

    lock = False

    stopWatchdog = False
    messageToShow = None

    # INFO Composing the app
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Label(
            "TransTerm - A simple terminal-based YouTube downloader and transcriber by TheCookingSenpai\n",
            classes="title",
        )
        yield Label(
            "Yellow -> idle • Red -> busy • Green -> success\n\n",
            classes="status_yellow",
            id="status",
        )
        # Inputs

        yield Label("Enter a YouTube link to work with:")
        yield Input(
            placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            id="link",
        )
        # Configuration
        yield Horizontal(
            Checkbox(
                'Download a playlist',
                id="downloadPlaylist",
            ),
            Checkbox(
                "Convert to mp3",
                id="toMp3",
            ),
            Checkbox(
                "Convert to wav",
                id="toWav",
            ),
            Checkbox(
                "Transcript to text",
                id="toText",
            ),
        )
        options = [
            ("Google Simple", "google"),
            ("Google with silence detection", "google_silence"),
            ("Local (using Sphynx)", "local"),
        ]
        yield Select(options, id="engine")
        # Buttons
        yield Button("Go", id="go")
        yield Button("Exit", id="exit")
        # Infos
        yield Label("Video title: ", id="video_title")
        yield Label("Video author: ", id="video_author")
        yield Label("Video length: ", id="video_length")
        yield Label("Configuration: ", id="configuration")
        random.seed(73)
        data = [random.expovariate(1 / 3) for _ in range(1000)]
        yield Sparkline(data, summary_function=mean, id="divisor")
        yield RichLog(id="main_log")

    # SECTION Actions
    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # sourcery skip: extract-method, switch
        """Handle button events."""
        action = str(event.button.id).lower()
        if action == "exit":
            try:
                term.forceQuit = True
            except Exception:
                print("[SYSTEM] Failed to stop thread")
            exit(1)
        elif action == "go":
            if self.lock:
                self.query_one("#main_log").write("Already working!")
                return
            self.lock = True
            status = self.query_one("#status")
            status.classes = "status_red"
            status.text = "Status: working..."
            self.query_one("#main_log").write("Proceeding...")
            self.query_one("#main_log").write("Params extraction...")
            self.process = threading.Thread(name="act", target=self.act)
            self.query_one("#main_log").write("Started!")
            self.process.start()

    def act(self):
        link = self.query_one("#link")
        link = link.value
        if link == "":
            link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.query_one("#main_log").write(f"Link: {link}")
        toMp3 = self.query_one("#toMp3")
        toMp3 = toMp3.value
        toWav = self.query_one("#toWav")
        toWav = toWav.value
        toText = self.query_one("#toText")
        toText = toText.value
        isPlaylist = self.query_one("#downloadPlaylist")
        isPlaylist = isPlaylist.value

         # Branching: in playlist mode we download (and if needed convert) all the videos of the playlist
        # TODO NOTE: Transcribing is intentionally disabled on playlists. Feel free to tinker but it's a risk.

        # TODO: Avoid redundancy with the below branch
        if isPlaylist:
            self.query_one("#main_log").write("Downloading playlist...")
            if toMp3 or toWav:
                self.query_one("#main_log").write(
                    "Converting to mp3 only too (wav is not supported on playlists)...this may take a while"
                )
            playlist = term.printPlaylist(link)
            print(playlist)
            self.query_one("#main_log").write("Please note that the TUI might seems frozen while downloading the playlist. Check the downloads folder for the progress.")
            self.query_one("#main_log").write("...Yes, we are working on it.")
            # TODO More verbosity!
            d_path = term.managePlaylist(playlist, to_download=True, to_convert=toMp3 or toWav)
            status = self.query_one("#status")
            status.classes = "status_green"
            self.query_one("#main_log").write("Done!")
            self.query_one("#main_log").write(str(d_path))
            self.lock = False
            return

        # Branching: in single video mode we download (and if needed convert) the video
        self.query_one("#main_log").write(f"MP3: {toMp3}, WAV: {toWav}, TEXT: {toText}")
        try:
            infos = term.getInfo(link)
        except Exception as e:
            self.query_one("#main_log").write(
                "ERROR: Could not retrieve informations: " + str(e) + ";"
            )
            return

        self.query_one("#video_title").value = "Title: " + infos["title"]
        self.query_one("#video_author").value = "Author: " + infos["author"]
        self.query_one("#video_length").value = "Seconds: " + infos["length"]
        self.query_one("#configuration").value = (
            "\n" + f"MP3: {toMp3}, WAV: {toWav}, TEXT: {toText}"
        )


        # First we download the video
        folder = term.download(link)
        # Now, if the user wants to convert to mp3, we do it
        if toMp3:
            self.query_one("#main_log").write(
                "Converting to mp3...this may take a while"
            )
            term.convert(folder, format="mp3")
        # Now, if the user wants to convert to wav or text, we do it
        if toWav and not toText:
            self.query_one("#main_log").write(
                "Converting to wav...this may take a while"
            )
            file = term.convert(folder, format="wav")
        # Now, if the user wants to convert to text, we do it
        if toText:
            self.query_one("#main_log").write(
                "Converting to text...this may take a while"
            )
            engine = self.query_one("#engine").value
            file = term.convert(folder, format="wav")
            if engine == "google_silence":
                self.query_one("#main_log").write("Using Google with silence detection")
                file = term.get_large_audio_transcription_on_silence(folder)
            elif engine == "local":
                self.query_one("#main_log").write("Using Sphynx CMU")
                file = term.local_audio_transcribe(folder)
            else:
                self.query_one("#main_log").write("Using Google Simple")
                file = term.simple_audio_transcribe(folder)
        status = self.query_one("#status")
        status.classes = "status_green"
        self.query_one("#main_log").write("Done!")
        self.query_one("#main_log").write(str(file))
        self.lock = False
        return True

    # !SECTION Actions

    def loadEnv(self):
        self.env = {}
        with open(".env", "r") as f:
            textenv = f.readlines()
            for line in textenv:
                key, value = line.split("=")
                self.env[key.strip()] = value.strip()

    def saveEnv(self):  # sourcery skip: use-join
        preparedEnv = ""
        for key, value in self.env.items():
            preparedEnv += f"{key}={value}" + "\n"
        with open(".env", "w") as f:
            f.write(preparedEnv)
            f.flush()
        return self.env


if __name__ == "__main__":
    app = TransTerm()
    app.loadEnv()
    app.run()
