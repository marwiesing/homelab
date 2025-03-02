Below is a concise summary of the steps you followed to install and configure PostgreSQL on your Ubuntu server with a custom data directory on your SSD:

---

### PostgreSQL Installation & Configuration Summary

1. **Install PostgreSQL Packages:**
   - Update the package list and install PostgreSQL:
     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```
   - Verify the installation:
     ```bash
     psql --version
     ```

2. **Stop the PostgreSQL Service:**
   - Stop PostgreSQL to prepare for reconfiguration:
     ```bash
     sudo systemctl stop postgresql
     ```

3. **Remove the Existing Cluster (if necessary):**
   - Drop the default "main" cluster to move the data directory:
     ```bash
     sudo pg_dropcluster --stop 16 main
     ```

4. **Prepare the New Data Directory:**
   - Create a subdirectory on your SSD mount (avoiding the lost+found directory):
     ```bash
     sudo mkdir -p /mnt/postgres/data
     sudo chown -R postgres:postgres /mnt/postgres/data
     ```

5. **Create a New PostgreSQL Cluster on the SSD:**
   - Initialize a new cluster with its data stored on `/mnt/postgres/data`:
     ```bash
     sudo pg_createcluster --datadir=/mnt/postgres/data 16 main
     ```

6. **Start PostgreSQL Service:**
   - Start PostgreSQL and verify the cluster is using the new data directory:
     ```bash
     sudo systemctl start postgresql
     pg_lsclusters
     ```
   - The output should indicate that the “main” cluster is online and its data directory is `/mnt/postgres/data`.

7. **Test the Installation:**
   - Log in to PostgreSQL:
     ```bash
     sudo -u postgres psql
     ```
   - Run a simple query (e.g., `SELECT version();`) to confirm everything is working.

---

This summary provides a quick reference to the process you followed. You can refer back to these steps whenever you need to reinstall or modify your PostgreSQL configuration on your Ubuntu server.