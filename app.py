import os
from datetime import timedelta
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

AUDIO_FILE = "DHH_LEX_Interview.wav"

SPEAKER_COLORS = ["cyan", "magenta", "green", "yellow", "blue", "red"]

console = Console()

def format_timestamp(seconds: float, format_type="vtt") -> str:
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)

    if format_type == "srt":
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def write_webvtt_file(utterances, output_file="output.vtt"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for utt in utterances:
            start = format_timestamp(utt.start, "vtt")
            end = format_timestamp(utt.end, "vtt")
            speaker = utt.speaker if hasattr(utt, "speaker") else 0
            transcript = utt.transcript

            f.write(f"{start} --> {end}\n")
            f.write(f"<v Speaker {speaker}>{transcript}\n\n")
    print(f"✅ [green]WEBVTT file saved as:[/green] {output_file}")

def write_srt_file(utterances, output_file="output.srt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, utt in enumerate(utterances, start=1):
            start = format_timestamp(utt.start, "srt")
            end = format_timestamp(utt.end, "srt")
            transcript = utt.transcript

            f.write(f"{idx}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{transcript}\n\n")
    print(f"✅ [green]SRT file saved as:[/green] {output_file}")

def display_transcript_rich(utterances):
    print("\n[bold underline]📝 Transcript Preview:[/bold underline]\n")
    for utt in utterances:
        speaker = utt.speaker if hasattr(utt, "speaker") else 0
        color = SPEAKER_COLORS[speaker % len(SPEAKER_COLORS)]
        start = format_timestamp(utt.start)
        end = format_timestamp(utt.end)
        header = f"Speaker {speaker} [{start} - {end}]"

        console.print(Panel(utt.transcript, title=header, border_style=color))

def main():
    try:
        print("[bold blue]\n🎙️ Deepgram Subtitle Generator[/bold blue]")
        print("[dim]------------------------------------------[/dim]\n")

        # Step 1: Create Deepgram client
        deepgram = DeepgramClient()

        file_path = Prompt.ask("Enter path to audio file", default=AUDIO_FILE)

        with open(file_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # Step 2: Transcribe
        options = PrerecordedOptions(
            model="nova-3",
            smart_format=True,
            utterances=True,
            diarize=True,
        )
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        utterances = response.results.utterances

        display_transcript_rich(utterances)

        # Step 3: Format choice
        print("\nChoose subtitle format:")
        print("1. SRT (.srt)")
        print("2. WEBVTT (.vtt)")
        choice = Prompt.ask("Enter 1 or 2", choices=["1", "2"])

        if choice == "1":
            write_srt_file(utterances, output_file="output.srt")
        else:
            write_webvtt_file(utterances, output_file="output.vtt")

    except Exception as e:
        print(f"❌ [red]Exception occurred:[/red] {e}")

if __name__ == "__main__":
    main()

