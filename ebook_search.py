import os
import argparse
import warnings

from srv.ebook_services import clear_db, delete_table, get_database_size, init_table, init_index, query_database, insert_doc_to_db, reindex
from utils.epub2txt import epub2txt
from utils.pdf2txt import pdf2txt
from tqdm import tqdm

def insert_pdf_to_db(pdf_path: str, verbose: bool = False) -> None:
    if verbose:
        print('Converting PDF to TXT...')
    txt_path = pdf2txt(pdf_path)
    if verbose:
        print(f'Successfully converted {pdf_path} to {txt_path}')
    insert_doc_to_db(txt_path, verbose=verbose)
    print('Added document to database.')
    os.remove(txt_path)
    if verbose:
        print(f'Temporary file {txt_path} deleted.')

def insert_epub_to_db(epub_path: str, verbose: bool = False) -> None:
    if verbose:
        print('Converting EPUB to TXT...')
    txt_path = epub2txt(epub_path)
    if verbose:
        print(f'Successfully converted {epub_path} to {txt_path}')
    insert_doc_to_db(txt_path, verbose=verbose)
    print('Added document to database.')
    os.remove(txt_path)
    if verbose:
        print(f'Temporary file {txt_path} deleted.')

def main():
    parser = argparse.ArgumentParser(description='Vector Database Management')
    parser.add_argument('-c', '--clear', action='store_true', help='Clear the database')
    parser.add_argument('-i', '--index', action='store_true', help='Create an index on the database')
    parser.add_argument('-r', '--reindex', action='store_true', help='Recreate the index on the database')
    parser.add_argument('-t', '--table', action='store_true', help='Create a table in the database')
    parser.add_argument('-x', '--drop-table', action='store_true', help='Drop the table in the database')
    parser.add_argument('-a', '--add', type=str, help='Add a document to the database')
    parser.add_argument('-d', '--dir', type=str, help='Add all files in a directory to the database')
    parser.add_argument('-q', '--query', type=str, help='Query the database with a question')
    parser.add_argument('--book', action='store_true', help='Flag for query option that queries whole books instead of text chunks')
    parser.add_argument('-n', '--num-results', type=int, default=5, help='Number of results to return for a query')
    parser.add_argument('--data-size', action='store_true', help='Print the size of the database')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')

    args = parser.parse_args()

    if args.clear:
        confirmation = input("Are you sure you want to clear the database? This action cannot be undone. (y/n): ")
        if confirmation.lower() != 'y':
            print('Clear database action aborted.')
            return
        clear_db()
        return
    
    if args.index:
        init_index()
        return
    
    if args.reindex:
        reindex()
        return
    
    if args.table:
        init_table()
        return
    
    if args.drop_table:
        confirmation = input("Are you sure you want to drop the table? This action cannot be undone. (y/n): ")
        if confirmation.lower() != 'y':
            print('Drop table action aborted.')
            return
        delete_table()
        return

    if args.add:
        if os.path.isfile(args.add):
            if args.add.endswith('.epub'):
                insert_epub_to_db(args.add, verbose=args.verbose)
            elif args.add.endswith('.pdf'):
                insert_pdf_to_db(args.add, verbose=args.verbose)
            elif args.add.endswith('.txt'):
                insert_doc_to_db(args.add, verbose=args.verbose)
        return

    if args.dir:
        files = [file for file in os.listdir(args.dir)]
        progress_bar = tqdm(files, desc="Processing files", unit="file")
        for file in progress_bar:
            progress_bar.set_description(f"Processing {file}")
            if file.endswith('.epub'):
                txt_path = epub2txt(os.path.join(args.dir, file))
            elif file.endswith('.pdf'):
                txt_path = pdf2txt(os.path.join(args.dir, file))
            elif file.endswith('.txt'):
                txt_path = os.path.join(args.dir, file)
            else:
                continue
            insert_doc_to_db(txt_path)
            os.remove(txt_path)
        return
    
    if args.query:
        results = query_database(args.query, args.num_results, args.verbose, args.book)
        print(f"Found {len(results)} results:")
        if args.book:
            for result in results:
                print(f"Document: {result['title']}\nDistance: {result['similarity']}\n")
            return
        else:
            for result in results:
                print(f"Document: {result['title']} Distance: {result['similarity']}\nContent: {result['text']}\n")
        return
    
    if args.data_size:
        size = get_database_size()
        print(f"Database size: {size}")
        return

if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib.epub")
    warnings.filterwarnings("ignore", category=FutureWarning, module="ebooklib.epub")
    main()