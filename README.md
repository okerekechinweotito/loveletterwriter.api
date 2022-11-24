# loveletterwriter.api

# loveletterwriter.api

How to Configure your database:
   We have hard-coded the database variables into the database.py, that means you need to create your database in postgresql.
   If you are new to postgresql, follow these steps to install

##### On windows

    1. Go to [postgresql website](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) and download postgresql database version >13.7
    2. Install with adminstrator priviledges and set your superuser password
    3. open pgAdmin 4
    <br><br>
    
    <br><br>
     - click server, and right click you PostgreSQL version
     - create new database and input your superuser password

4. Take note of your postgresql database_name, database_username, password and port(usually 5432).
Go to your `.env` file and type the following <br>
   SQLALCHEMY_DATABASE_URL="postgresql://<'database_username'>:<'your_password'>@localhost:port/database_name
