import psycopg2
import pandas as pd
import sqlparse as sp
import os


class PostgresDatabaseConnection():
    def __init__(self):
        self.database_host = os.getenv("PSQL_HOST") 
        self.database_name = os.getenv("PSQL_DB") 
        self.database_user = os.getenv("PSQL_USER")
        self.database_password = os.getenv("PSQL_PASSWORD")
        self.database_port = os.getenv("PSQL_PORT")
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        try:
            connection = psycopg2.connect(
                host=self.database_host,
                dbname=self.database_name,
                user=self.database_user,
                password=self.database_password,
                port=self.database_port
            )
            print(f'Connection established to PostgreSQL: {self.database_name}')
            return connection
        except Exception as e:
            print("Error while connecting to PostgreSQL", e)
            return None  # Return None in case of error

    def read_sql_query(self, query):
        if self.connection:
            try:
                return pd.read_sql_query(query, self.connection)
            except Exception as e:
                print("Error while executing query", e)
                return None
        else:
            print("No database connection available.")
            return None

    def execute_query(self, query):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    self.connection.commit()
            except Exception as e:
                print("Error while executing query", e)
                self.connection.rollback()
        else:
            print("No database connection available.")
            return None

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
                print("Database connection closed.")
            except Exception as e:
                print("Error while closing the connection", e)

# Example usage
if __name__ == "__main__":
    db = PostgresDatabaseConnection()

    with db.connection.cursor() as cursor:
        cursor.execute("SELECT current_user;")
        print("Connected as:", cursor.fetchone())

 
    with open("create_table.sql", "r") as file:
        sql_script = file.read()


    # Use sqlparse to split the script into individual statements
    commands = sp.split(sql_script)
    for command in commands:
        print(command)
        command = command.strip()
        if command:
            db.execute_query(command)


    db.disconnect()
