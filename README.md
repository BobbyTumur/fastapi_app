Sep 13

The fastapi project as a noob.
Connected fastapi and mysql with tortoise-orm, using authentication method JWT(JSON web token)
Note: this project is not complete, as the testing codes are not implemented yet. Deployment in docker would be the last as the all implementation is finished. 

To launch the application you need to:

1. MYSQL running 

VM commands:
    sudo apt update
    sudo systemctl install mysql-server -y
    sudo sed -i 's/^bind-address\s*=.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
        alternatively: sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
                       change manually bind-address = 127.0.0.1 to 0.0.0.0
    sudo sysmtectl restart mysql
    sudo mysql -u root

MYSQL commands: *TIPS: create username, password, database name by replacing the part starting from star and ending with star, make sure delete the stars too  
    CREATE DATABASE ★database name★;
    CREATE USER '★username★'@'%' IDENTIFIED BY '★username password★';
    GRANT ALL PRIVILEGES ON ★database name, same as above★.* TO '★username★'@'%';
    FLUSH PRIVILEGES;

2. Create the .env file in the folder with credentials you created on step 1.

# Database URL
DATABASE_URL=mysql://★username★:★password★@★IP address of the VM that is running MYSQL★/★database name★

# Secret key for JWT encoding/decoding
SECRET_KEY="★COPY PASTE THE RANDOM KEY BY RUNNING THIS COMMAND, openssl rand -base64 64★"

# Algorithm for JWT encoding #openssl rand -base64 64
ALGORITHM=HS256

# Token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES=15

3. Lastly Python virtual environment running

Python CLI commands:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    uvicorn main:app --reload