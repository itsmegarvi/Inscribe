import json
import os
import shutil
import tarfile
import tempfile
from contextlib import closing
from pathlib import Path

try:
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import HTTPError, Request, urlopen

INSCRIBE_DIR = Path(__file__).parent.resolve()
DATA_DIR = INSCRIBE_DIR / "sample_data"
INSCRIBE_RELEASES_API = "https://api.github.com/repos/IgnisDa/Inscribe/releases/latest"


def colored_print(color, message):
    colors = dict(
        SUCCESS="\033[92m",
        INFO="\033[96m",
        WARNING="\033[93m",
        FAIL="\033[91m",
        END="\033[0m",
    )

    if color not in colors:
        raise ValueError(f"The color should be among {list(colors.keys())}")
    print(colors[color] + message + colors["END"], flush=True)


class Downloader:
    def get_download_url(self):
        request = Request(INSCRIBE_RELEASES_API, headers={"User-Agent": "INSCRIBE"})

        with closing(urlopen(request)) as response:
            data = json.loads(response.read())
        gzip_name = "sample_data.tar.gz"
        assets = data["assets"]
        for asset in assets:
            if asset["name"] == gzip_name:
                return asset["browser_download_url"], gzip_name

    def download_release(self):
        gzip_url, gzip_name = self.get_download_url()
        try:
            r = urlopen(gzip_url)
        except HTTPError as e:
            if e.code == 404:
                raise RuntimeError("Could not find {} file".format(gzip_name))

        meta = r.info()
        size = int(meta["Content-Length"])
        colored_print(
            "INFO",
            "  - Downloading {} ({:.2f} MB)".format(gzip_name, size / 1024 / 1024),
        )

        with self.inscribe_temp_directory() as dir_:
            tar = os.path.join(dir_, gzip_name)
            with open(tar, "wb") as f:
                block_size = 8192
                current = 0
                while True:
                    buffer = r.read(block_size)
                    if not buffer:
                        break
                    current += len(buffer)
                    f.write(buffer)
            return tar

    def install(self):
        colored_print("INFO", "Installing sample data...")
        inscribe_tar = self.download_release()
        with tarfile.open(inscribe_tar, "r:gz") as tar_file:
            temporary_dir = self.inscribe_temp_directory()
            colored_print("WARNING", "Starting extraction... It might take some time...")
            tar_file.extractall(temporary_dir)
            shutil.move(temporary_dir / "sample_data", DATA_DIR)
        colored_print("SUCCESS", "Sample data installed on your system successfully!")

    def inscribe_temp_directory(self):
        return Path(tempfile.mkdtemp())


if __name__ == "__main__":
    downloader = Downloader()
    downloader.install()
