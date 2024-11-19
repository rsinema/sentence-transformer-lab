import os
import pandas as pd
from db.db_methods import check_db_size, create_index, create_table, drop_table, fast_pg_insert, query_similar_books, query_similar_chunks, remove_index, clear_table
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Get the model name from the environment variable
MODEL_NAME = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')

def _chunk_text(text, n=500, overlap=50):
    '''
        Split a text into overlapping chunks of length n.

        Parameters:
        text (str): The text to split into chunks.
        n (int): The length of each chunk.
        overlap (int): The number of characters to overlap between chunks.

        Returns:
        List[str]: A list of overlapping text chunks.
    '''
    return [text[i:i+n] for i in range(0, len(text), n-overlap)]

def _process_doc(file_path):
    '''
        Process a document by loading it from disk, splitting it into chunks, and processing each chunk.

        Parameters:
        file_path (str): The path to the file to process.

        Returns:
        List[str]: A list of processed text chunks.
    '''
    
    text = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    chunks = _chunk_text(text)
    chunks = [' '.join(chunk.split()) for chunk in chunks]
    return chunks

def _embed_doc(file_path, model, verbose=False):
    '''
        Embed a document by loading it from disk, splitting it into chunks, and embedding each chunk.

        Parameters:
        file_path (str): The path to the file to embed.
        model (SentenceTransformer): The sentence transformer model to use for embedding.

        Returns:
        Tuple[List[str], List[np.array]]: A tuple containing a list of text chunks and a list of chunk embeddings.
    '''
    if verbose:
        print(f'Embedding {file_path}...')
    chunks = _process_doc(file_path)
    return chunks, model.encode(chunks)

def _prepare_doc_for_db(file_path, model, verbose=False):
    '''
        Prepare a document for database insertion by embedding it and creating a DataFrame.

        Parameters:
        file_path (str): The path to the file to process.
        model (SentenceTransformer): The sentence transformer model to use for embedding.

        Returns:
        pd.DataFrame: A DataFrame containing the embeddings and associated metadata.
    '''
    chunks, embeddings = _embed_doc(file_path, model, verbose)
    title = os.path.basename(file_path)

    embeddings_list = [embedding.tolist() for embedding in embeddings]

    # This is throwing an error because the embeddings are not in the correct format
    data = {
        'book_title': [title] * len(chunks),
        'chunk_text': chunks,
        'chunk_number': [int(x) for x in range(1, len(chunks) + 1)],
        'embedding': embeddings_list
    }
    return pd.DataFrame(data)

def insert_doc_to_db(file_path, columns=['book_title', 'chunk_text', 'chunk_number', 'embedding'], verbose=False):
    '''
        Process a document, prepare it for database insertion, and insert it into the database.

        Parameters:
        file_path (str): The path to the file to process.
        model (SentenceTransformer): The sentence transformer model to use for embedding.
        columns (List[str]): A list of column names in the target table that correspond to the DataFrame columns.

        Returns:
        None
    '''
    if verbose:
        print('Loading model...')
    model = SentenceTransformer(MODEL_NAME)
    if verbose:
        print("Begining insertion process...")
    df = _prepare_doc_for_db(file_path, model, verbose)
    if verbose:
        print("Inserting chunks...")
    fast_pg_insert(df, columns)

def query_database(query, n=5, verbose=False, books=False):
    '''
        Query the database for documents containing the given text.

        Parameters:
        query (str): The text to search for in the database.

        Returns:
        List[Tuple[str, str]]: A list of tuples containing the document title and the matching text.
    '''
    if verbose:
        print('Loading model...')
    model = SentenceTransformer(MODEL_NAME)
    if verbose:
        print('Embedding query...')
    query_embedding = model.encode([query])[0].tolist()
    if verbose:
        print('Querying database...')
    if books:
        results = query_similar_books(query_embedding, n)
        results_dict = [{'title': result[0], 'text': 'N/A', 'similarity': result[2]} for result in results]
    else:
        results = query_similar_chunks(query_embedding, n)
        results_dict = [{'title': result[0], 'text': result[1], 'similarity': result[2]} for result in results]
    
    return results_dict

def init_table():
    '''
        Initialize the database by creating the table for document embeddings.

        Parameters:
        None

        Returns:
        None
    '''
    print('Creating table...')
    create_table()
    print('Table created.')

def init_index():
    '''
        Initialize the database index for the embeddings column.

        Parameters:
        None

        Returns:
        None
    '''
    print('Creating index...')
    create_index()
    print('Index created.')

def reindex():
    '''
        Recreate the database index for the embeddings column.

        Parameters:
        None

        Returns:
        None
    '''
    print('Recreating index...')
    remove_index()
    create_index()
    print('Index recreated.')

def clear_db():
    '''
        Clear the PostgreSQL table of all data.

        Parameters:
        None

        Returns:
        None
    '''
    print('Clearing database...')
    remove_index()
    clear_table()
    print('Database cleared.')

def delete_table():
    '''
        Drop the PostgreSQL table for storing book embeddings.

        Parameters:
        None

        Returns:
        None
    '''
    print('Dropping table...')
    drop_table()
    print('Table dropped.')

def get_database_size():
    '''
        Get the size of the database in a human-readable format.

        Parameters:
        None

        Returns:
        str: The size of the database.
    '''
    print('Querying database size...')
    return check_db_size()