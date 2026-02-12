# **Wrong folder structure, fix it later**

# FLAC Audio Chunking & Whisper Transcription

This project chunks FLAC audio files into 20-second segments and transcribes them using OpenAI's Whisper LLM via HuggingFace Inference API.

## Features

- **Audio Chunking**: Splits FLAC files into configurable 20-second segments using PyDub
- **Whisper Integration**: Sends each chunk to Whisper LLM for transcription
- **Results Management**: Writes all transcriptions to a formatted text file
- **File Protection**: Results file is set to read-only after creation

## Prerequisites

1. **Python 3.8+**
2. **FFmpeg**: Required by PyDub for audio processing
   - macOS: `brew install ffmpeg`
   - Linux: `apt-get install ffmpeg`
   - Windows: Download from https://ffmpeg.org/download.html

3. **HuggingFace Credentials**:
   - Create account at https://huggingface.co
   - Get HF Token from https://huggingface.co/settings/tokens
   - Set up HF Inference endpoint for Whisper

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables** in `.env` file:
   ```
   HF_TOKEN=your_huggingface_token_here
   HF_INFERENCE_ENDPOINT=your_inference_endpoint_url_here
   ```

3. **Prepare Audio Files**:
   - Place FLAC files in the `audio/` folder
   - Ensure files are in FLAC format (.flac extension)

## Usage

Run the main script:
```bash
python chunk_and_transcribe.py
```

### What the Script Does

1. Scans the `audio/` folder for FLAC files
2. For each FLAC file:
   - Creates chunks of 20 seconds
   - Saves chunks to `chunks/{filename_without_extension}/` folder
3. Processes all chunks through Whisper LLM API
4. Writes results to `transcription_results.txt` (read-only)

### Output

- **Chunks**: Stored in `chunks/{original_filename}/` directory
- **Transcriptions**: Saved to `transcription_results.txt`
  - Formatted with chunk names and transcription results
  - Timestamp of generation included
  - File is automatically set to read-only

## File Structure

```
chunk-script/
├── audio/                          # Place FLAC files here
├── chunks/                         # Generated chunk files
├── sciprt2.py                      # Original script (reference)
├── chunk_and_transcribe.py         # Main processing script
├── transcription_results.txt       # Output file (read-only)
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in repo)
└── README.md                       # This file
```

## Configuration

Edit `chunk_and_transcribe.py` to customize:

- **Chunk Length**: Change `chunk_length = 20` (in seconds)
- **Audio Folder**: Change `audio_folder = "audio"`
- **Chunks Folder**: Change `chunks_folder = "chunks"`
- **Output File**: Change `output_text_file = "transcription_results.txt"`

## Troubleshooting

### "FFmpeg not found"
- Install FFmpeg (see Prerequisites section)

### "No FLAC files found"
- Verify files are in `audio/` folder
- Check file extension is `.flac`

### API Errors
- Verify HF_TOKEN is correct in `.env`
- Check HF_INFERENCE_ENDPOINT URL is valid
- Ensure you have API credits/access

### Permission Denied on Output File
- The file is intentionally read-only. Change permissions if needed:
  ```bash
  chmod u+w transcription_results.txt
  ```

## Original References

- Original script: `sciprt2.py`
- Reference chunking code provided
- Built with PyDub and Whisper LLM integration

## Notes

- Each chunk is processed sequentially for reliable API handling
- Results include both successful transcriptions and any errors
- File timestamps help track when transcriptions were created
- Read-only status prevents accidental modification of results

