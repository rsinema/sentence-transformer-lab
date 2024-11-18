import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import argparse

def epub2txt(epub_path):
    """
    Convert an EPUB file to text format.
    
    Args:
        epub_path (str): Path to the EPUB file
        
    Returns:
        str: Filename of the generated text file
    """
    # Read EPUB file
    book = epub.read_epub(epub_path)
    
    # Storage for extracted text
    chapters = []
    
    # Iterate through all items in the EPUB
    for item in book.get_items():
        # We're only interested in HTML content (the text of the book)
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Get the content
            html_content = item.get_content()

            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Get text content and remove extra whitespace
            text = ' '.join(soup.get_text().split())
            
            # Add to chapters if there's actual content
            if text.strip():
                chapters.append(text)
    
    # Join all chapters with newlines
    for c in chapters:
        print(c[:100])
    text_content = '\n\n'.join(chapters)
    txt_filename = os.path.splitext(os.path.basename(epub_path))[0] + '.txt'
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(text_content)

    return txt_filename

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Convert EPUB files to TXT files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python script.py -f /path/to/epub/files/file.epub
        '''
    )
    
    parser.add_argument(
        '-f', '--file',
        help='EPUB file to convert'
    )

    # Parse arguments
    args = parser.parse_args()
    
    # Convert files
    if (args.file):
        # Convert single file
        if not os.path.isfile(args.file):
            parser.error(f"Input file does not exist: {args.file}")
        text_file = epub2txt(args.file)
    else:
        parser.error("Please provide either a file or directory to convert")

if __name__ == "__main__":
    main()