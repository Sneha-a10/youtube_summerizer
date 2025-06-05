import os
import logging

# Configure logging
logging.basicConfig(filename='cleanup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def cleanup_files(files_to_delete):
    """
    Deletes the specified files.
    """
    for filename in files_to_delete:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                logging.info(f"Deleted file: {filename}")
                print(f"Deleted file: {filename}")
            else:
                logging.info(f"File not found, skipping: {filename}")
                print(f"File not found, skipping: {filename}")
        except Exception as e:
            logging.error(f"Error deleting {filename}: {e}")
            print(f"Error deleting {filename}: {e}")

def main():
    files_to_delete = ['summary.txt', 'transcription.txt']
    cleanup_files(files_to_delete)

if __name__ == "__main__":
    main()