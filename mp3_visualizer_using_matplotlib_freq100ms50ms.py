import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

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
    
    return energies, log_bands

def visualize_mp3_over_time(file_path, chunk_size_ms=50, num_bands=8):
    audio = AudioSegment.from_mp3(file_path)
    sample_rate = audio.frame_rate
    
    # Analyze the entire audio file in chunks
    time_energies = []
    for i in range(0, len(audio), chunk_size_ms):
        chunk = audio[i:i+chunk_size_ms]
        energies, log_bands = analyze_chunk(chunk, sample_rate, num_bands)
        time_energies.append(energies)
    
    time_energies = np.array(time_energies).T
    time_energies = time_energies / np.max(time_energies)
    
    band_labels = [f"{int(log_bands[i])}-{int(log_bands[i+1])} Hz" for i in range(num_bands)]
    
    plt.figure(figsize=(20, 10))
    plt.imshow(time_energies, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(label='Normalized Energy')
    plt.title(f'MP3 Time-Frequency Visualization (Chunk size: {chunk_size_ms}ms)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency Bands')
    
    plt.yticks(range(num_bands), band_labels)
    
    total_chunks = time_energies.shape[1]
    seconds = np.arange(0, total_chunks * chunk_size_ms / 1000, 5)
    plt.xticks(seconds * (1000 / chunk_size_ms), [f"{s:.0f}s" for s in seconds])
    
    plt.tight_layout()
    plt.savefig(f'time_frequency_visualization_{chunk_size_ms}ms.png', dpi=300)
    print(f"Visualization saved as time_frequency_visualization_{chunk_size_ms}ms.png")

# Usage
file_path = "/home/study/projects/Sleigh-Ride.mp3"
visualize_mp3_over_time(file_path, chunk_size_ms=50)  # Try 50ms chunks
visualize_mp3_over_time(file_path, chunk_size_ms=100)  # Compare with 100ms chunks
