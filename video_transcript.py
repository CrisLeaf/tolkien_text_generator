import subprocess


command = "ffmpeg -i youtube_video.webm -ab 160k -ar 44100 -vn audio.wav"
subprocess.call(command, shell=True)

#%%
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


r = sr.Recognizer()

def get_large_audio_transcription(path):
	"""
	Splitting the large audio file into chunks and apply speech recognition
	on each of these chunks.
	"""
	# Open the audio file using pydub
	sound = AudioSegment.from_wav(path)
	
	# Split audio sound where silence is 700 miliseconds or more and get chunks
	chunks = split_on_silence(
		sound,
		min_silence_len=500,
		silence_thresh=sound.dBFS-14,
		keep_silence=500
	)
	
	# Create a directory to store the audio chunks
	folder_name = "audio-chunks"
	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)
	whole_text = ""
	
	# Process each chunk
	for i, audio_chunk in enumerate(chunks, start=1):
		
		# Export audio chunk and save it in the "folder_name" directory
		chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
		audio_chunk.export(chunk_filename, format="wav")
		
		# Recognize the chunk
		with sr.AudioFile(chunk_filename) as source:
			audio_listened = r.record(source)
			
			# try converting it to text
			try:
				text = r.recognize_google(audio_listened, language="es-ES")
			except sr.UnknownValueError as e:
				print("Error:", str(e))
			else:
				text = f"{text.capitalize()}."
				print(chunk_filename, ":", text)
				whole_text += text
				
	# return the text for all chunks detected
	return whole_text

#%%
path = "audio.wav"
print("\nFull text:", get_large_audio_transcription(path))
