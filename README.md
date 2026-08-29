# Agriculture

This repository stores simple agriculture data and a small ETL script.

What this does:
- Adds a Python ETL script to load sample agriculture data into a MySQL database.

How to run (simple):
1. Install requirements: `pip install pandas sqlalchemy pymysql`
2. Edit database settings at the top of `scripts/etl_pipeline.py` (user, password, host, port, name).
3. Make sure your MySQL server is running and the database exists.
4. Run the script: `python scripts/etl_pipeline.py`

If you need help, open an issue.
