import scrapetube
import pytube
import random
import typer
import json
import pathlib
import time
import subprocess
import sys

app = typer.Typer()


def startfile(path):
    opener = "open" if sys.platform == "darwin" else "xdg-open"

    subprocess.call([opener, path])


def assure_dirs():
    pathlib.Path.home().joinpath(".local", "hamza", "videos").mkdir(
        parents=True, exist_ok=True
    )


def get_videos_data():
    with open(
        pathlib.Path(pathlib.Path.home(), ".local", "hamza", "config.json")
    ) as file:
        return json.load(file)


def get_random_video():
    return random.choice(get_videos_data())


assure_dirs()

HAMZA_CHANNEL_ID = "UCWsslCoN3b_wBaFVWK_ye_A"


@app.command()
def info():
    video_data = get_videos_data()

    print(f"Videos indexed: {len(video_data)}")
    print(f"Videos downloaded: 0")
    print(f"Videos watched: 0")


@app.command()
def setup():
    print("This could take a couple of minutes...")

    videos = scrapetube.get_channel(HAMZA_CHANNEL_ID)

    video_data = []

    counter = 0

    for video in videos:
        video_important_data = {
            "video_id": video["videoId"],
            "video_url": f"https://www.youtube.com/watch?v={video['videoId']}",
            "video_title": video["title"]["runs"][0]["text"],
            "video_length": video["lengthText"]["simpleText"],
        }

        video_data.append(video_important_data)

        counter = counter + 1

        if not counter % 5:
            print(
                f"We are already in the video number {counter}! (Last one is \"{video_important_data['video_title']}\")"
            )

            time.sleep(2)

    json_data = json.dumps(video_data, indent=4)

    with open(
        pathlib.Path(pathlib.Path.home(), ".local", "hamza", "config.json"), "w"
    ) as data_file:
        data_file.write(json_data)

    print("Setup complete!")


@app.command()
def watch():
    video = get_random_video()

    vid_path = str(
        pathlib.Path.home().joinpath(
            ".local", "hamza", "videos", f"{video['video_id']}.mp4"
        )
    )

    print(f"You are about to watch '{video['video_title']}'.")

    stream = (
        pytube.YouTube(video["video_url"])
        .streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )

    if not stream:
        return

    stream.download(vid_path)

    typer.launch(vid_path)

    print("Enjoy :)")


app()
