#!/usr/bin/env python3
"""
normalize.py

Recursively scans a folder for .mp3/.m4a files and normalizes each file's
volume to a target dBFS level (default: -20.0 dBFS). Overwrites the
original files in place.

Dependencies:
    - pydub (pip install pydub)
    - ffmpeg (e.g. brew install ffmpeg)

Usage:
    python3 normalize.py /path/to/your/music/folder [--target-dbfs TARGET]
    python3 normalize.py /Users/niklaskloiber/Music/Music/Media.localized --target-dbfs -20

"""

import os
import sys
import argparse
from pydub import AudioSegment

def get_audio_extension(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".mp3":
        return "mp3"
    elif ext == ".m4a":
        return "m4a"
    else:
        return None  # or raise an exception if you only expect these types

"""
 @see https://www.ffmpeg.org/general.html#File-Formats
 for file format info
"""
def get_audio_export_format(filename):
    ext = get_audio_extension(filename)
    
    if ext == "mp3":
        return "mp3"
    elif ext == "m4a":
        return "ipod"


def match_target_amplitude(sound: AudioSegment, target_dBFS: float) -> AudioSegment:
    """
    Normalize given AudioSegment to target dBFS.

    :param sound: AudioSegment instance
    :param target_dBFS: desired average loudness in dBFS (negative float, e.g. -20.0)
    :return: normalized AudioSegment
    """
    change_in_dBFS = target_dBFS - sound.dBFS
    print(f" → Old dbfs: {sound.dBFS:.2f}, delta: {change_in_dBFS:.2f}")
    if change_in_dBFS > -1 and change_in_dBFS < 1:
        return None

    return sound.apply_gain(change_in_dBFS)

def normalize_folder(folder: str, target_dBFS: float):
    """
    Walk through `folder`, find all music files, normalize them, and overwrite.

    :param folder: path to the root directory containing music files
    :param target_dBFS: desired loudness level in dBFS
    """
    # Walk directory tree
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith(".mp3") or filename.lower().endswith(".m4a"):
                file_path = os.path.join(root, filename)
                print(f"Normalizing: {file_path}")

                try:
                    audio = AudioSegment.from_file(file_path, format=get_audio_extension(filename))
                    normalized_audio = match_target_amplitude(audio, target_dBFS)

                    if normalized_audio == None:
                        print(f" → Nothing done. Target dBFS didn't differ that much from current dBFS\n")
                    else:
                        normalized_audio.export(file_path, format=get_audio_export_format(filename))
                        print(f" → Done (new dBFS: {normalized_audio.dBFS:.2f})\n")
                except Exception as e:
                    if hasattr(e, 'message'):
                        print(f" → Error reading or processing file: {e.message}\n")
                    else:
                        print(f" → Error reading or processing file: {e}\n")
            else:
                print(f"File was not known audio file. Filename: {os.path.join(root, filename)}\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Normalize volume of all MP3 files in a folder."
    )
    parser.add_argument(
        "folder",
        help="Absolute or relative path to folder containing music files",
    )
    parser.add_argument(
        "--target-dbfs",
        type=float,
        default=-20.0,
        help="Target loudness in dBFS (default: -20.0)",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if not os.path.isdir(args.folder):
        print(f"Error: '{args.folder}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{args.folder}' for music files…")
    normalize_folder(args.folder, args.target_dbfs)
    print("All done!")

