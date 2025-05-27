import os

import pandas as pd
from sentence_transformers import SentenceTransformer

from db.db_methods import check_db_size
from db.db_methods import clear_books
from db.db_methods import clear_embeddings
from db.db_methods import create_index
from db.db_methods import drop_book_embeddings
from db.db_methods import drop_books_table
from db.db_methods import fast_pg_insert
from db.db_methods import get_book_text_by_title
from db.db_methods import init_books_table
from db.db_methods import initialize_book_embeddings_table
from db.db_methods import insert_book
from db.db_methods import query_similar_books
from db.db_methods import query_similar_chunks
from db.db_methods import remove_index

# Get the model name from the environment variable
MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
CHUNK_LENGTH = int(os.getenv("CHUNK_LENGTH", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))


def _chunk_text(text, n=500, overlap=50):
    """
    Split a text into overlapping chunks of length n.

    Parameters:
    text (str): The text to split into chunks.
    n (int): The length of each chunk.
    overlap (int): The number of characters to overlap between chunks.

    Returns:
    List[str]: A list of overlapping text chunks.
    """
    return [text[i : i + n] for i in range(0, len(text), n - overlap)]


def _process_doc(file_path):
    """
    Process a document by loading it from disk, splitting it into chunks, and processing each chunk.

    Parameters:
    file_path (str): The path to the file to process.

    Returns:
    List[str]: A list of processed text chunks.
    """

    text = ""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = _chunk_text(text, CHUNK_LENGTH, CHUNK_OVERLAP)
    chunks = [" ".join(chunk.split()) for chunk in chunks]
    return chunks


def _embed_doc(file_path, model, verbose=False):
    """
    Embed a document by loading it from disk, splitting it into chunks, and embedding each chunk.

    Parameters:
    file_path (str): The path to the file to embed.
    model (SentenceTransformer): The sentence transformer model to use for embedding.

    Returns:
    Tuple[List[str], List[np.array]]: A tuple containing a list of text chunks and a list of chunk embeddings.
    """
    if verbose:
        print(f"Embedding {file_path}...")
    chunks = _process_doc(file_path)
    return chunks, model.encode(chunks)


def _prepare_doc_for_db(file_path, model, verbose=False):
    """
    Prepare a document for database insertion by embedding it and creating a DataFrame.

    Parameters:
    file_path (str): The path to the file to process.
    model (SentenceTransformer): The sentence transformer model to use for embedding.

    Returns:
    pd.DataFrame: A DataFrame containing the embeddings and associated metadata.
    """
    chunks, embeddings = _embed_doc(file_path, model, verbose)
    title = os.path.basename(file_path)

    chunk_offsets = []
    curr_offset = 0
    for chunk in chunks:
        chunk_offsets.append(curr_offset)
        curr_offset += len(chunk) + 1 - CHUNK_OVERLAP

    embeddings_list = [embedding.tolist() for embedding in embeddings]

    data = {
        "book_title": [title] * len(chunks),
        "chunk_text": chunks,
        "chunk_number": [int(x) for x in range(1, len(chunks) + 1)],
        "begin_offset": chunk_offsets,
        "embedding": embeddings_list,
    }
    return pd.DataFrame(data)


def insert_doc_to_db(
    file_path,
    columns=["book_title", "chunk_text", "chunk_number", "begin_offset", "embedding"],
    verbose=False,
):
    """
    Process a document, prepare it for database insertion, and insert it into the database.

    Parameters:
    file_path (str): The path to the file to process.
    model (SentenceTransformer): The sentence transformer model to use for embedding.
    columns (List[str]): A list of column names in the target table that correspond to the DataFrame columns.

    Returns:
    None
    """
    if verbose:
        print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)
    if verbose:
        print("Begining insertion process...")
    df = _prepare_doc_for_db(file_path, model, verbose)
    if verbose:
        print("Inserting chunks...")
    title = os.path.basename(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    insert_book(title, text)
    fast_pg_insert(df, columns)


def query_database(query, n=5, verbose=False, books=False, extended=False):
    """
    Query the database for documents containing the given text.

    Parameters:
    query (str): The text to search for in the database.

    Returns:
    List[Tuple[str, str]]: A list of tuples containing the document title and the matching text.
    """
    if verbose:
        print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)
    if verbose:
        print("Embedding query...")
    query_embedding = model.encode([query])[0].tolist()
    if verbose:
        print("Querying database...")
    if books:
        results = query_similar_books(query_embedding, n)
        results_dict = [{"title": result[0], "text": "N/A", "similarity": result[2]} for result in results]
    elif extended:
        chunk_results = query_similar_chunks(query_embedding, n)
        results_dict = []
        curr_title = ""
        for result in chunk_results:
            if result[0] != curr_title:
                curr_title = result[0]
            book_text = get_book_text_by_title(curr_title)
            offset = result[3]

            start = max(0, offset - CHUNK_LENGTH)
            end = min(len(book_text), offset + CHUNK_LENGTH)

            results_dict.append(
                {
                    "title": result[0],
                    "text": book_text[start:end],
                    "similarity": result[2],
                }
            )
    else:
        results = query_similar_chunks(query_embedding, n)
        results_dict = [{"title": result[0], "text": result[1], "similarity": result[2]} for result in results]

    return results_dict


def init_table():
    """
    Initialize the database by creating the table for document embeddings.

    Parameters:
    None

    Returns:
    None
    """
    print("Creating tables...")
    init_books_table()
    initialize_book_embeddings_table()
    print("Tables created.")


def init_index():
    """
    Initialize the database index for the embeddings column.

    Parameters:
    None

    Returns:
    None
    """
    print("Creating index...")
    create_index()
    print("Index created.")


def reindex():
    """
    Recreate the database index for the embeddings column.

    Parameters:
    None

    Returns:
    None
    """
    print("Recreating index...")
    remove_index()
    create_index()
    print("Index recreated.")


def clear_db():
    """
    Clear the PostgreSQL table of all data.

    Parameters:
    None

    Returns:
    None
    """
    print("Clearing database...")
    remove_index()
    clear_embeddings()
    clear_books()
    print("Database cleared.")


def delete_table():
    """
    Drop the PostgreSQL table for storing book embeddings.

    Parameters:
    None

    Returns:
    None
    """
    print("Dropping tables...")
    drop_book_embeddings()
    drop_books_table()
    print("Tables dropped.")


def get_database_size():
    """
    Get the size of the database in a human-readable format.

    Parameters:
    None

    Returns:
    str: The size of the database.
    """
    print("Querying database size...")
    return check_db_size()
