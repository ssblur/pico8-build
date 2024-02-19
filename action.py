from urllib.request import urlopen
from os import getenv
from json import loads
from platform import system, architecture, uname, platform
from ssl import _create_unverified_context
from zipfile import ZipFile
from os.path import isfile
from subprocess import run

TOKEN = getenv("PICO8_TOKEN")
OUTPUT = getenv("PICO8_OUTPUT")
INPUT = getenv("PICO8_INPUT")

def main():
    if not OUTPUT:
        print("Please specify env variable PICO8_OUTPUT")
        exit(1)
    if not INPUT:
        print("Please specify env variable PICO8_INPUT")
        exit(1)

    if not isfile("./pico8.zip"):
        if not TOKEN:
            print("Please specify env variable PICO8_TOKEN or provide pico8.zip")
            exit(1)

        data = urlopen(f"https://www.humblebundle.com/api/v1/order/{TOKEN}").read()
        data = loads(data)

        download_url = ""
        for download in data["subproducts"][0]["downloads"]:
            if download["platform"] == system().lower():
                for option in download["download_struct"]:
                    if (
                        option["name"] == "zip"
                        or option["name"] == "raspi" and uname()[4].startsWith("arm")
                        or option["name"] == "64-bit" and architecture()[0] == "64bit"
                        or option["name"] == "32-bit" and architecture()[0] == "32bit"
                    ):
                        download_url = option["url"]["web"]

        with open("pico8.zip", "wb") as f:
            f.write(urlopen(download_url, context=_create_unverified_context()).read())

    with ZipFile("pico8.zip", "r") as f:
        f.extractall(".")

    if platform().startswith("Windows"):
        run(["pico-8/pico8.exe", "-export", OUTPUT, INPUT])
    else:
        run(["pico-8/pico8", "-export", OUTPUT, INPUT])

if __name__ == "__main__":
    main()