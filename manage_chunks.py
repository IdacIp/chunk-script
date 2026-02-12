#!/usr/bin/env python3
"""
Utility script to manage chunks and results
"""

import os
import shutil
import argparse
from pathlib import Path

def clean_chunks(chunks_folder="chunks"):
    """Delete all generated chunks"""
    if os.path.exists(chunks_folder):
        shutil.rmtree(chunks_folder)
        print(f"Deleted {chunks_folder} folder and all chunks.")
    else:
        print(f"{chunks_folder} folder not found.")

def clean_results(results_file="transcription_results.txt"):
    """Delete results file"""
    if os.path.exists(results_file):
        # Make writable first if read-only
        os.chmod(results_file, 0o644)
        os.remove(results_file)
        print(f"Deleted {results_file}")
    else:
        print(f"{results_file} not found.")

def make_results_writable(results_file="transcription_results.txt"):
    """Make results file writable"""
    if os.path.exists(results_file):
        os.chmod(results_file, 0o644)
        print(f"Made {results_file} writable.")
    else:
        print(f"{results_file} not found.")

def list_audio_files(audio_folder="audio"):
    """List FLAC files in audio folder"""
    if not os.path.exists(audio_folder):
        print(f"{audio_folder} folder not found.")
        return

    flac_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(".flac")]

    if not flac_files:
        print(f"No FLAC files in {audio_folder}")
    else:
        print(f"Found {len(flac_files)} FLAC file(s):")
        for f in flac_files:
            file_path = os.path.join(audio_folder, f)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"  - {f} ({size_mb:.2f} MB)")

def list_chunks(chunks_folder="chunks"):
    """List generated chunks"""
    if not os.path.exists(chunks_folder):
        print(f"{chunks_folder} folder not found.")
        return

    total_chunks = 0
    for root, dirs, files in os.walk(chunks_folder):
        flac_files = [f for f in files if f.lower().endswith(".flac")]
        if flac_files:
            folder_name = os.path.basename(root)
            print(f"\n{folder_name}: {len(flac_files)} chunks")
            total_chunks += len(flac_files)

    if total_chunks == 0:
        print(f"No chunks found in {chunks_folder}")
    else:
        print(f"\nTotal: {total_chunks} chunks")

def main():
    parser = argparse.ArgumentParser(description="Utility for managing audio chunks and transcriptions")
    parser.add_argument("--clean-chunks", action="store_true", help="Delete all generated chunks")
    parser.add_argument("--clean-results", action="store_true", help="Delete results file")
    parser.add_argument("--make-writable", action="store_true", help="Make results file writable")
    parser.add_argument("--list-audio", action="store_true", help="List FLAC files in audio folder")
    parser.add_argument("--list-chunks", action="store_true", help="List generated chunks")

    args = parser.parse_args()

    if args.clean_chunks:
        clean_chunks()
    elif args.clean_results:
        clean_results()
    elif args.make_writable:
        make_results_writable()
    elif args.list_audio:
        list_audio_files()
    elif args.list_chunks:
        list_chunks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

