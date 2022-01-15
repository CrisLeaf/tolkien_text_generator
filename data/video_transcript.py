import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


def get_large_audio_transcription(file):
	"""
	Splitting the large audio file into chunks and apply speech recognition
	on each of these chunks.
	"""
	# Open the audio file using pydub
	sound = AudioSegment.from_wav(file)
	
	# Split audio sound where silence is 700 miliseconds or more and get chunks
	chunks = split_on_silence(
		sound,
		min_silence_len=500,
		silence_thresh=sound.dBFS-14,
		keep_silence=500
	)
	
	# Create a directory to store the audio chunks
	folder_name = file[0:-4] + "_chunks"
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
				print("Error", str(e))
			else:
				text = f"{text.capitalize()}."
				print(chunk_filename, " Done.")
				whole_text += text
				
	# return the text for all chunks detected
	return whole_text


if __name__ == "__main__":
	r = sr.Recognizer()
	
	files = os.listdir("wav_data")
	files = [file for file in files if file[-6:] != "chunks"]
	
	for filename in files:
		print("Converting " + filename + "...")
		whole_text = get_large_audio_transcription("wav_data/" + filename)
		
		with open("text_data/text_data.txt", "a") as f:
			f.write(whole_text)
			f.write("\n")
	
	print("Done!")