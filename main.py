import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import re
# import pyttsx3

# engine = pyttsx3.init()

# def configure_tts_engine(engine):
#     # List available voices
#     voices = engine.getProperty('voices')
#     for index, voice in enumerate(voices):
#         print(f"Voice {index}: {voice.name} - {voice.id}")

#     # Set properties
#     engine.setProperty('voice', voices[1].id)  # Change index to select a different voice
#     engine.setProperty('rate', 150)  # Speed of speech (default is usually around 200)
#     engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# def read_text_file_aloud(file_path):
#     configure_tts_engine(engine)

#     # Open the text file and read its content
#     with open(file_path, 'r', encoding='utf-8') as file:
#         text = file.read()

#     # Use the TTS engine to say the text
#     engine.say(text)
#     engine.runAndWait()

def extract_chapters_from_epub(file_path):
    book = epub.read_epub(file_path)
    chapters = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            title = soup.title.string if soup.title else "Chapter"
            text = soup.get_text().strip()
            
            # Filter out empty chapters or chapters with very little content
            if len(text) < 200:  # you can adjust this threshold
                continue
            
            # Filter out chapters that are likely to be numbers/glossary
            if re.match(r'^\d+$', title) or 'glossary' in title.lower():
                continue
            if 'copyright' in text.lower() and len(text) < 2000:
                continue
            
            chapters.append((title, text))

    return chapters

def clean_filename(filename):
    # Remove invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def save_chapters_to_files(chapters, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, (title, text) in enumerate(chapters):
        # Clean the title to create a valid filename
        filename = clean_filename(f"{i+1:02d}_{title[:50].replace(' ', '_')}.txt")
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Saved: {file_path}")

if __name__ == "__main__":
    input_file_path = 'input/SiloSrs.epub'
    output_dir = 'output'

    chapters = extract_chapters_from_epub(input_file_path)
    save_chapters_to_files(chapters, output_dir)
    print(f"Chapters have been successfully saved to {output_dir}")

    # file_path = 'output_chapters/01_Chapter.txt'
    # read_text_file_aloud(file_path)