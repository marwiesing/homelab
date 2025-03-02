Here's a concise summary of working with PostgreSQL on an Ubuntu server using the command line:

- **Connecting to the Database:**  
  Use the built-in `psql` client. For example:  
  ```bash
  sudo -u postgres psql
  ```  
  Once inside, you can run SQL commands directly.

- **Basic psql Commands:**  
  - List databases: `\l`  
  - Connect to a specific database: `\c dbname`  
  - List tables: `\dt`  
  - Describe a table: `\d tablename`  
  - Quit: `\q`

- **Managing Databases:**  
  Use SQL statements to create, update, and delete databases and tables. For example:  
  ```sql
  CREATE DATABASE mydb;
  CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT);
  INSERT INTO users (name) VALUES ('Alice');
  SELECT * FROM users;
  ```

- **Backup and Restore:**  
  - Backup: Use `pg_dump mydb > mydb.sql`  
  - Restore: Use `psql mydb < mydb.sql` or `pg_restore` for custom formats.

- **Server Management:**  
  Control the PostgreSQL service with system commands:  
  ```bash
  sudo systemctl start postgresql
  sudo systemctl stop postgresql
  sudo systemctl status postgresql
  ```

- **Configuration & Logs:**  
  - Configuration files are typically located in `/etc/postgresql/16/main`.  
  - Log files are in `/var/log/postgresql/`.

- **No Built-in UI:**  
  By default, PostgreSQL on Ubuntu is managed via the command line. While there isn’t a built-in graphical tool, you can install third-party UIs like pgAdmin4 or DBeaver if you need a GUI later.  

This approach gives you full control using terminal commands, which is both lightweight and powerful for server environments.