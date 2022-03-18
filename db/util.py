import psycopg2
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)


def connect():
    """
    Creates a connection to the PostgreSQL database
    """
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    return psycopg2.connect(database=db_name, user=db_user, password=db_password)


def bulk_insert(df, table):
    """
    Used to bulk insert a pandas DataFrame into the DB.
    :param df: The DataFrame to be inserted
    :param table: The name of the database table
    """
    conn = connect()
    cur = conn.cursor()
    tuple_lst = [tuple(x) for x in df.to_numpy()]  # Create a list of tuples from the DataFrame
    cols = ','.join(list(df.columns))  # Comma separated column names
    str_template = ','.join(['%s' for _ in range(len(tuple_lst[0]))])  # Template to string format the tuples

    args_str = ','.join([cur.mogrify(f"({str_template})", tup).decode('utf8') for tup in tuple_lst])
    query = f"INSERT INTO {table}({cols}) VALUES {args_str}"
    cur.execute(query, tuple_lst)

    conn.commit()
    cur.close()
    conn.close()


def exec_sql_file(path):
    """
    Executes a SQL file at the provided path
    :param path: String path to the SQL file
    """
    full_path = os.path.join(os.path.dirname(__file__), path)
    conn = connect()
    cur = conn.cursor()
    with open(full_path, 'r') as file:
        cur.execute(file.read())
    conn.commit()
    cur.close()
    conn.close()


exec_sql_file('init.sql')
