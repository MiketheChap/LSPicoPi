import json
import struct
import os

def create_minimal_lshow(filename):
    # Create a minimal JSON structure
    data = {
        "frames": [
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
        ] * 2  # Repeat the pattern only 2 times
    }
    
    json_data = json.dumps(data).encode('utf-8')
    
    with open(filename, 'wb') as f:
        # Write magic number
        f.write(b"LSHW")
        
        # Write JSON length
        f.write(struct.pack('<I', len(json_data)))
        
        # Write JSON data
        f.write(json_data)
        
        # No dummy audio data this time

    print(f"Minimal test file created: {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")

create_minimal_lshow("minimal_test.lshow")
