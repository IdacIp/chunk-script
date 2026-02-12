import requests
import base64
import os
import json
import stat
from pydub import AudioSegment
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)

# Set up machine and get the credentials from https://huggingface.co/openai/whisper-large-v3-turbo -> HF Inference
# FLAC files should be in the "audio" folder

def query(payload):
    """Send audio chunk to Whisper LLM endpoint"""
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + str(os.getenv("HF_TOKEN")),
        "Content-Type": "application/json"
    }
    response = requests.post(
        os.getenv("HF_INFERENCE_ENDPOINT"),
        headers=headers,
        json=payload
    )
    return response.json()

def chunk_flac_audio(input_file, output_folder, chunk_length_s=20):
    """Chunk a FLAC file into segments"""
    print(f"Loading {input_file}...")
    audio = AudioSegment.from_file(input_file, format="flac")

    # Calculate details (pydub works in milliseconds)
    chunk_length_ms = chunk_length_s * 1000
    total_length_ms = len(audio)

    # Calculate number of chunks
    num_chunks = (total_length_ms // chunk_length_ms) + (1 if total_length_ms % chunk_length_ms != 0 else 0)

    print(f"Total duration: {total_length_ms/1000:.2f} seconds")
    print(f"Generating {num_chunks} chunks...")

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunks = []
    # Slice and save
    for i in range(num_chunks):
        start_time = i * chunk_length_ms
        end_time = (i + 1) * chunk_length_ms

        chunk = audio[start_time:end_time]

        # Format filename (e.g., chunk_001.flac)
        output_filename = os.path.join(output_folder, f"chunk_{i+1:03d}.flac")

        # Export the chunk
        chunk.export(output_filename, format="flac")
        print(f"Exported: {output_filename}")
        chunks.append(output_filename)

    print("Chunking complete.\n")
    return chunks

def process_chunks_with_whisper(chunk_files, output_text_file):
    """Process all chunks through Whisper LLM and save results"""
    results = []

    print("Starting transcription of chunks...\n")

    for chunk_file in chunk_files:
        try:
            print(f"Processing chunk: {os.path.basename(chunk_file)}")

            # Read chunk file and encode to base64
            with open(chunk_file, "rb") as f:
                base_64_encoded = base64.b64encode(f.read())
                base_64_str = base_64_encoded.decode('utf-8')

            # Query Whisper API
            output = query({
                "inputs": base_64_str,
                "parameters": {}
            })

            print(f"Successfully converted {os.path.basename(chunk_file)} to text.")
            results.append({
                "chunk_file": os.path.basename(chunk_file),
                "transcription": output
            })

        except Exception as e:
            print(f"Error processing {chunk_file}: {str(e)}")
            results.append({
                "chunk_file": os.path.basename(chunk_file),
                "error": str(e)
            })

    print(f"\nTranscription complete. Writing results to {output_text_file}...\n")

    # Write results to text file
    with open(output_text_file, "w") as f:
        f.write(f"Whisper LLM Transcription Results\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            chunk_name = result["chunk_file"]
            f.write(f"Chunk: {chunk_name}\n")
            f.write("-" * 80 + "\n")

            if "error" in result:
                f.write(f"ERROR: {result['error']}\n")
            else:
                f.write(json.dumps(result["transcription"], ensure_ascii=False, indent=2))

            f.write("\n\n")

    # Set file permissions to read-only
    set_readonly(output_text_file)

    print(f"Results saved to {output_text_file}")
    print(f"File permissions set to read-only.\n")

def set_readonly(filepath):
    """Set file to read-only (user can read, but cannot write)"""
    # Get current permissions
    current_perms = os.stat(filepath).st_mode
    # Set to read-only for owner (r--r--r--)
    os.chmod(filepath, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

def main():
    # Configuration
    audio_folder = "audio"
    chunks_folder = "chunks"
    output_text_file = "transcription_results.txt"
    chunk_length = 20  # seconds

    # Find all FLAC files in audio folder
    if not os.path.exists(audio_folder):
        print(f"Error: Audio folder '{audio_folder}' not found.")
        return

    flac_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(".flac")]

    if not flac_files:
        print(f"No FLAC files found in '{audio_folder}' folder.")
        return

    print(f"Found {len(flac_files)} FLAC file(s) to process.\n")

    all_chunks = []

    # Process each FLAC file
    for flac_file in flac_files:
        input_path = os.path.join(audio_folder, flac_file)
        file_chunks_folder = os.path.join(chunks_folder, os.path.splitext(flac_file)[0])

        print(f"\n{'='*80}")
        print(f"Processing: {flac_file}")
        print(f"{'='*80}\n")

        # Chunk the audio file
        chunks = chunk_flac_audio(input_path, file_chunks_folder, chunk_length)
        all_chunks.extend(chunks)

    # Process all chunks through Whisper
    if all_chunks:
        process_chunks_with_whisper(all_chunks, output_text_file)
        print("All processing complete!")
    else:
        print("No chunks were created.")

if __name__ == "__main__":
    main()

