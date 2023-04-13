#!/usr/bin/env python3.10

import sys
import os
import argparse
from datetime import datetime
from mimetypes import guess_type

try:
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
except:
    print("Please install AudioSegment before using. e.g. 'pip (or pip3) install AudioSegment'");
    sys.exit(1)

def split_sound(wav_path, dir_path, silence_dur, silence_th):
    # convert wav to AudioSegment obj.
    seg = AudioSegment.from_wav(wav_path)

    # split chunks
    chunks = split_on_silence(seg, min_silence_len=silence_dur, silence_thresh=silence_th)
    for i, ch in enumerate(chunks):
        ch.export(f"{dir_path}/{i:05}.wav", format="wav")

def ensure_dir(path, prog):
    if path == None:
        d = prog + "-output-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        os.makedirs(d)
        return d
    if os.path.exists(path) == True:
        if os.path.isdir(path) == True:
            return path
        else:
            print("\n" + "The file having the same name, '{}' exists. Stopped processing.".format(path) + "\n")
            sys.exit(1)
    else:
        if os.path.isdir(path) == False:
            print("\n" + "Could not find the directory '{}'. Do you want to create it? [Y/n]".format(path))
            while True:
                c = sys.stdin.read(1)
                if c == "Y" or c == "y" or ord(c) == 10:
                    os.makedirs(path)
                    return path
                elif c == "N" or c == "n":
                    print("\n" + "Stopped processing." + "\n")
                    sys.exit(1)
                else:
                    print("\n" + "Please input Y or N.")

def check_wav(path, help):
    if os.path.exists(path) == False:
        print("\n" + "Could not find the file '{}'.".format(path) + "\n")
        help()
        sys.exit(1)
    if guess_type(path)[0] != 'audio/x-wav':
        print("\n" + "The file '{}' is not a WAV file.".format(path) + "\n")
        help()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description = "Split a WAV file into multiple WAV files by silent duration.")
    parser.add_argument("wav_path",
        help = "Path of a WAV file to be split.")
    parser.add_argument("--duration", "-d",
        type = int,
        default = 500,
        help = "Duration of silence as delimiter in millisecond (default: 500)")
    parser.add_argument("--threshold", "-t",
        type = int,
        default = -40,
        help = "Threshold of sound volume as silence in dBFS (default: -40)")

    args = parser.parse_args()

    check_wav(args.wav_path, parser.print_help)
    output_dir = ensure_dir(None, parser.prog)

    split_sound(args.wav_path, output_dir, args.duration, args.threshold)

if __name__ == "__main__":
    main()
