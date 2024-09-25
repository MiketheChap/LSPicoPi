# LSPicoPi
This is a revision of LightShowPi (https://bitbucket.org/togiles/lightshowpi/), software designed for the Raspberry Pi Pico microcontroller. Hopefully, it will require fewer dependencies than LightSHowPi and the Raspberry Pi.

Given this prompt, Claude provided the following framework:
"If i wanted to create a box that would take songs in mp3 format, use ffmpeg to create and save a file reflecting a spectrum of 8 frequencies. When turned on, the circuit would trigger relays corresponding to 8 strands/channels of conventional leds. It would randomize playback of the songs."

"That's an interesting project idea! You're essentially describing a custom audio visualizer that analyzes music and controls LED strips based on frequency content. Here's a high-level overview of how you could approach this:

Audio Input and Processing:

Use a microcontroller or single-board computer (like Raspberry Pi) to read MP3 files.
Utilize FFmpeg to convert MP3 to raw audio data.
Implement a Fast Fourier Transform (FFT) to analyze the frequency content.


Frequency Analysis:

Divide the audio spectrum into 8 frequency bands.
Calculate the energy/amplitude in each band.


LED Control:

Map each frequency band to a relay controlling an LED strip.
Adjust LED brightness or patterns based on the energy in each band.


Playback System:

Implement a simple file system to store and access MP3 files.
Create a randomization function for song selection.


Hardware:

Use a microcontroller with sufficient processing power and storage.
Include 8 relays to control the LED strips.
Add an amplifier and speaker for audio output.



Here's a basic pseudocode outline for the main loop:
"while True:
    randomSong = selectRandomSong()
    rawAudio = convertMp3ToRawAudio(randomSong)
    
    while audioStillPlaying:
        frequencyData = performFFT(currentAudioChunk)
        energyLevels = calculateEnergyLevels(frequencyData)
        
        for i in range(8):
            if energyLevels[i] > threshold:
                activateRelay(i)
            else:
                deactivateRelay(i)
        
        playAudioChunk()
        
    waitForNextSong()"


Given these requirements, Claude proposed the following:
import json
from pydub import AudioSegment
import numpy as np

def analyze_song(mp3_file, num_channels=8, chunk_ms=50):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file)
    
    # Convert to mono for simplicity
    audio = audio.set_channels(1)
    
    # Prepare the output data structure
    output_data = []
    
    # Process the audio in chunks
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i+chunk_ms]
        
        # Convert to numpy array
        samples = np.array(chunk.get_array_of_samples())
        
        # Perform FFT
        fft_result = np.fft.fft(samples)
        magnitude_spectrum = np.abs(fft_result)
        
        # Divide into frequency bands
        band_energies = np.array_split(magnitude_spectrum[:len(magnitude_spectrum)//2], num_channels)
        
        # Calculate energy in each band
        energy_levels = [int(np.sum(band)) for band in band_energies]
        
        # Normalize energy levels to 0-255 range for LED brightness
        max_energy = max(energy_levels)
        if max_energy > 0:
            energy_levels = [int((e / max_energy) * 255) for e in energy_levels]
        
        output_data.append(energy_levels)
    
    return output_data

def save_analysis(output_data, filename):
    with open(filename, 'w') as f:
        json.dump(output_data, f)

# Example usage
mp3_file = "path_to_your_song.mp3"
output_data = analyze_song(mp3_file)
save_analysis(output_data, "song_analysis.json")

# Arduino/RP2040 pseudocode for playback
"""
#include <ArduinoJson.h>

void setup() {
  // Initialize LED pins, file system, etc.
}

void loop() {
  // Read JSON file
  File file = SD.open("song_analysis.json");
  DynamicJsonDocument doc(MAX_FILE_SIZE);
  deserializeJson(doc, file);
  
  // Play audio file separately
  
  // Iterate through the analysis data
  for (JsonArray frame : doc.as<JsonArray>()) {
    for (int i = 0; i < 8; i++) {
      analogWrite(LED_PINS[i], frame[i].as<int>());
    }
    delay(50);  // Assuming 50ms chunks
  }
}
"""

Claude created and I tested the following on my Ubuntu system: 
1. Set up a location for your virtual environment where you will do song analysis, test, and create your JSON or other related files, then open that folder.
**cd /home/study/projects/mp3_analysis
python3 -m venv venv
source venv/bin/activate**
2. Install numpy
**pip install numpy matplotlib scipy pydub**
3. Create the following files:

