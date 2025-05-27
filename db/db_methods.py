import io
import os
from typing import List

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql://nlp_user:nlp_password@localhost:6012/nlp_db")
EMBEDDING_LENGTH = os.getenv("EMBEDDING_LENGTH", 384)

CREATE_EXTENSION = "CREATE EXTENSION IF NOT EXISTS vector;"

INITIALIZE_BOOK_EMBEDDINGS_TABLE = f"""
                CREATE TABLE IF NOT EXISTS book_embeddings (
                    id SERIAL PRIMARY KEY,
                    book_title TEXT,
                    chunk_text TEXT,
                    chunk_number INTEGER,
                    begin_offset INTEGER,
                    embedding vector({EMBEDDING_LENGTH}),
                    FOREIGN KEY (book_title) REFERENCES books(title)
                );
                """

DROP_BOOK_EMBEDDINGS = "DROP TABLE IF EXISTS book_embeddings;"

CREATE_INDEX = """
                CREATE INDEX IF NOT EXISTS embedding_idx ON book_embeddings
                USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64);
                """

REMOVE_INDEX = "DROP INDEX IF EXISTS embedding_idx;"

INSERT_DOC = """
             INSERT INTO book_embeddings (book_title, chunk_text, chunk_number, begin_offset, embedding)
             VALUES (%s, %s, %s, %s, %s);
             """

QUERY_SIMILAR_CHUNKS = """
                        SELECT book_title, chunk_text, embedding <=> %s::vector AS distance, begin_offset
                        FROM book_embeddings
                        ORDER BY distance
                        LIMIT %s;
                        """

QUERY_SIMILAR_BOOKS = """
                        SELECT book_title, AVG(embedding) AS avg_embedding, AVG(embedding) <=> %s::vector AS distance
                        FROM book_embeddings
                        GROUP BY book_title
                        ORDER BY distance
                        LIMIT %s;
                        """

CLEAR_ALL_EMBEDDINGS = "DELETE FROM book_embeddings;"

CHECK_DB_SIZE = "SELECT pg_size_pretty(pg_database_size(current_database()));"

CREATE_BOOKS_TABLE = """
                    CREATE TABLE IF NOT EXISTS books (
                        id SERIAL PRIMARY KEY,
                        title TEXT UNIQUE,
                        text TEXT
                    );
                    """

INSERT_BOOK = """
                INSERT INTO books (title, text)
                VALUES (%s, %s)
                ON CONFLICT (title) DO NOTHING;
                """

CLEAR_BOOKS = "DELETE FROM books;"

DROP_BOOKS = "DROP TABLE IF EXISTS books;"

GET_BOOK_TEXT_BY_TITLE = "SELECT text FROM books WHERE title = %s;"


def initialize_book_embeddings_table():
    """
    Create the PostgreSQL table for storing book embeddings.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_EXTENSION)
            cursor.execute(INITIALIZE_BOOK_EMBEDDINGS_TABLE)
            connection.commit()


def drop_book_embeddings():
    """
    Drop the PostgreSQL table for storing book embeddings.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(DROP_BOOK_EMBEDDINGS)
            connection.commit()


def create_index():
    """
    Create the PostgreSQL index for the book embeddings.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_INDEX)
            connection.commit()


def remove_index():
    """
    Remove the PostgreSQL index for the book embeddings.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(REMOVE_INDEX)
            connection.commit()


def clear_embeddings():
    """
    Clear the PostgreSQL table of all data.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CLEAR_ALL_EMBEDDINGS)
            connection.commit()


def insert_chunk(book_title, chunk_text, chunk_number, begin_offset, embedding):
    """
    Insert a document chunk into the PostgreSQL database.

    Parameters:
    book_title (str): The title of the book.
    chunk_text (str): The text of the chunk.
    chunk_number (int): The chunk number within the chapter.
    embedding (np.array): The embedding of the chunk.

    Returns:
    None
    """
    # Convert types before insertion
    chunk_number = int(chunk_number)  # Convert np.int64 to Python int

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    INSERT_DOC,
                    (book_title, chunk_text, chunk_number, begin_offset, embedding),
                )
                connection.commit()
                print(f"Successfully inserted chunk {chunk_number}")
            except Exception as e:
                print(f"Error inserting chunk: {e}")
                print(
                    f"Types: book_title={type(book_title)}, chunk_text={type(chunk_text)}, "
                    f"chunk_number={type(chunk_number)}, embedding={type(embedding)}"
                )
                connection.rollback()
                raise


def fast_pg_insert(df: pd.DataFrame, columns: List[str]) -> None:
    """
    Inserts data from a pandas DataFrame into a PostgreSQL table using the COPY command for fast insertion.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data to be inserted.
    connection (str): The connection string to the PostgreSQL database.
    table_name (str): The name of the target table in the PostgreSQL database.
    columns (List[str]): A list of column names in the target table that correspond to the DataFrame columns.

    Returns:
    None
    """
    conn = psycopg2.connect(CONNECTION_STRING)
    _buffer = io.StringIO()
    df.to_csv(
        _buffer,
        sep="\t",  # Use tab as separator instead of semicolon
        index=False,
        header=False,
        escapechar="\\",  # Add escape character
        doublequote=True,  # Handle quotes properly
        na_rep="\\N",  # Proper NULL handling
    )
    _buffer.seek(0)
    with conn.cursor() as c:
        c.copy_from(
            file=_buffer,
            table="book_embeddings",
            sep="\t",  # Match the separator used in to_csv
            columns=columns,
            null="\\N",  # Match the null representation
        )
    conn.commit()
    conn.close()


def query_similar_chunks(embedding, top_n=5):
    """
    Query the PostgreSQL database for similar embeddings.

    Parameters:
    embedding (np.array): The embedding to query for.
    top_n (int): The number of similar embeddings to return.

    Returns:
    List: A list of similar embeddings.
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_SIMILAR_CHUNKS, (embedding, top_n))
            results = cursor.fetchall()

    return results


def query_similar_books(embedding, top_n=5):
    """
    Query the PostgreSQL database for similar books.

    Parameters:
    embedding (np.array): The embedding to query for.
    top_n (int): The number of similar books to return.

    Returns:
    List: A list of similar books.
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(QUERY_SIMILAR_BOOKS, (embedding, top_n))
            results = cursor.fetchall()

    return results


def check_db_size():
    """
    Check the size of the PostgreSQL database.

    Parameters:
    None

    Returns:
    str: The size of the database in human-readable format.
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CHECK_DB_SIZE)
            size = cursor.fetchone()[0]

    return size


def init_books_table():
    """
    Create the PostgreSQL table for storing book texts.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BOOKS_TABLE)
            connection.commit()


def insert_book(title, text):
    """
    Insert a book into the PostgreSQL database.

    Parameters:
    title (str): The title of the book.
    text (str): The text of the book.

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_BOOK, (title, text))
            connection.commit()


def clear_books():
    """
    Clear the PostgreSQL table of all books.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CLEAR_BOOKS)
            connection.commit()


def drop_books_table():
    """
    Drop the PostgreSQL table for storing book texts.

    Parameters:
    None

    Returns:
    None
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(DROP_BOOKS)
            connection.commit()


def get_book_text_by_title(title):
    """
    Retrieve the text of a book from the PostgreSQL database.

    Parameters:
    title (str): The title of the book.

    Returns:
    str: The text of the book.
    """

    with psycopg2.connect(CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_BOOK_TEXT_BY_TITLE, (title,))
            text = cursor.fetchone()[0]

    return text
