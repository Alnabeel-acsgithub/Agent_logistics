import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_schema() -> str:
    """
    Retrieves the database schema including table names, columns, and relationships.
    
    Returns:
        A formatted string describing the database structure.
    """
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10
        )
        
        schema_info = []
        
        with connection:
            with connection.cursor() as cursor:
                # Get all tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                for table_dict in tables:
                    table_name = list(table_dict.values())[0]
                    schema_info.append(f"\n### Table: {table_name}")
                    
                    # Get columns for each table
                    cursor.execute(f"DESCRIBE `{table_name}`")
                    columns = cursor.fetchall()
                    
                    schema_info.append("Columns:")
                    for col in columns:
                        schema_info.append(f"  - {col['Field']} ({col['Type']}) {col['Key']} {col['Null']}")
                    
                    # Get sample row count
                    cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
                    count = cursor.fetchone()['count']
                    schema_info.append(f"Row count: {count}")
                
        return "\n".join(schema_info)
                
    except Exception as e:
        return f"Error retrieving schema: {e}"


def query_mysql_database(query: str) -> str:
    """
    Queries the MySQL database with the given SQL query.
    
    Args:
        query: The SQL query to execute.
        
    Returns:
        The result of the query as a string, or an error message.
    """
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10
        )
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                
                # Format results more readably
                if result:
                    return str(result)
                else:
                    return "Query executed successfully. No results returned."
                
    except Exception as e:
        return f"Error querying database: {e}"
