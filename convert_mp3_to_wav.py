import os
import subprocess
import sys

def convert_mp3_to_wav():
    # Source directory is the current directory
    source_dir = os.getcwd()
    output_dir = os.path.join(source_dir, "wav")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Find all mp3 files
    mp3_files = [f for f in os.listdir(source_dir) if f.lower().endswith(".mp3")]
    
    if not mp3_files:
        print("No MP3 files found in the current directory.")
        return

    print(f"Found {len(mp3_files)} MP3 files. Starting conversion...")

    success_count = 0
    error_count = 0

    for filename in mp3_files:
        mp3_path = os.path.join(source_dir, filename)
        wav_filename = os.path.splitext(filename)[0] + ".wav"
        wav_path = os.path.join(output_dir, wav_filename)

        # ffmpeg command
        # -i: input file
        # -acodec pcm_s16le: set audio codec to PCM 16-bit little-endian (standard WAV)
        # -ar 44100: set sample rate to 44.1kHz
        # -y: overwrite output file if it exists
        command = [
            "ffmpeg",
            "-i", mp3_path,
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-y",
            wav_path
        ]

        try:
            # Run ffmpeg, capture output to avoid cluttering terminal unless error
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Converted: {filename} -> {wav_filename}")
                success_count += 1
            else:
                print(f"Failed to convert: {filename}")
                print(f"Error: {result.stderr}")
                error_count += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            error_count += 1

    print("-" * 30)
    print("Conversion finished.")
    print(f"Successfully converted: {success_count}")
    print(f"Errors: {error_count}")
    
    if success_count == len(mp3_files):
        print("All files converted successfully.")
    else:
        print("Some files failed to convert. Please check the logs.")

if __name__ == "__main__":
    convert_mp3_to_wav()
