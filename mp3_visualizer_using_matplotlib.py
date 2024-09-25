import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pydub import AudioSegment
from pydub.playback import play
import threading

def analyze_chunk(chunk, sample_rate, num_bands=8):
    samples = np.array(chunk.get_array_of_samples())
    fft_result = np.fft.fft(samples)
    magnitude = np.abs(fft_result[:len(fft_result)//2])
    freqs = np.linspace(0, sample_rate/2, len(magnitude))
    
    min_freq = 20
    max_freq = sample_rate / 2
    log_bands = np.logspace(np.log10(min_freq), np.log10(max_freq), num_bands + 1)
    
    energies = []
    for i in range(num_bands):
        low, high = log_bands[i], log_bands[i+1]
        band_energy = np.sum(magnitude[(freqs >= low) & (freqs < high)]**2)
        energies.append(float(band_energy))
    
    return energies

def visualize_mp3(file_path, chunk_size_ms=50, num_bands=8):
    audio = AudioSegment.from_mp3(file_path)
    sample_rate = audio.frame_rate
    
    fig, ax = plt.subplots()
    bars = ax.bar(range(num_bands), [0] * num_bands)
    ax.set_ylim(0, 1)
    ax.set_title('MP3 Frequency Band Visualization')
    ax.set_xlabel('Frequency Bands')
    ax.set_ylabel('Normalized Energy')
    
    def update(frame):
        start = frame * chunk_size_ms
        chunk = audio[start:start+chunk_size_ms]
        energies = analyze_chunk(chunk, sample_rate, num_bands)
        normalized_energies = energies / max(energies) if max(energies) > 0 else energies
        for bar, energy in zip(bars, normalized_energies):
            bar.set_height(energy)
        return bars
    
    animation = FuncAnimation(fig, update, frames=len(audio)//chunk_size_ms, 
                              interval=chunk_size_ms, blit=True)
    
    def play_audio():
        play(audio)
    
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
    
    plt.savefig('visualization.png')
    print("Visualization saved as visualization.png")
    audio_thread.join()

# Usage
file_path = "/home/study/projects/Sleigh-Ride.mp3"
visualize_mp3(file_path)
