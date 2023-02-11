import scrapetube
import json
import pathlib
import time
import subprocess
import sys


def startfile(path):
    opener = "open" if sys.platform == "darwin" else "xdg-open"

    subprocess.call([opener, path])


HAMZA_CHANNEL_ID = "UCWsslCoN3b_wBaFVWK_ye_A"


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

    pathlib.Path(f"{pathlib.Path.home()}", ".local", "hamza").mkdir(
        parents=True, exist_ok=True
    )

    json_data = json.dumps(video_data, indent=4)

    with open(
        pathlib.Path(f"{pathlib.Path.home()}", ".local", "hamza","config.json"), "w"
    ) as data_file:
        data_file.write(json_data)

    print("Setup complete!")


setup()
