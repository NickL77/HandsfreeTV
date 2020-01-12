import pyaudio
import wave
import sys
from pydub import AudioSegment


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = 'file.wav'
FLAC_OUTPUT_FILENAME = 'file.flac'

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        frames_per_buffer=CHUNK)

print('recording...')
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print('finished recording')

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

song = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
song.export(FLAC_OUTPUT_FILENAME, format='flac')


