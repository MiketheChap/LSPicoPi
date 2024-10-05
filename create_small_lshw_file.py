import json
import struct

def create_test_lshow(filename):
    # Create a simple JSON structure
    data = {
        "frames": [
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
        ] * 50  # Repeat the pattern 50 times
    }
    
    json_data = json.dumps(data).encode('utf-8')
    
    with open(filename, 'wb') as f:
        # Write magic number
        f.write(b"LSHW")
        
        # Write JSON length
        f.write(struct.pack('<I', len(json_data)))
        
        # Write JSON data
        f.write(json_data)
        
        # Write some dummy audio data (just a short beep)
        f.write(b'\x00' * 1000)

    print(f"Test file created: {filename}")

create_test_lshow("test_lshow.lshow")
