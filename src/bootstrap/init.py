import subprocess
import sys
from src.bootstrap.check_depend import check_depend
from src.bootstrap.create_folder import create_folder


def init():
    is_ok, missing = check_depend()

    if not is_ok:
        print(f"Missing packages detected: {missing}")
        for package in missing:
            print(f"Downloading: {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Successfully installed: {package}")
            except Exception:
                print(f"Failed to install: {package}")

    create_folder()