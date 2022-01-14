import subprocess
import os


def convert_mp3_to_wav():
	files = os.listdir("mp3_data")
	
	for i, file in enumerate(files):
		subprocess.call(["ffmpeg", "-i", "mp3_data/" + file, f"wav_data/audio{i+1}.wav"])


if __name__ == "__main__":
	print("Converting files...")
	convert_mp3_to_wav()
	print("Done!")