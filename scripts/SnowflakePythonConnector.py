import snowflake.connector

# Set up connection parameters
CONNECTION_PARAMS = {
    'user': 'YOUR_USERNAME',
    'password': 'YOUR_PASSWORD',
    'account': 'YOUR_ACCOUNT_URL',
    'warehouse': 'YOUR_WAREHOUSE',
    'database': 'YOUR_DATABASE',
    'schema': 'YOUR_SCHEMA',
}

# Establish a connection
con = snowflake.connector.connect(**CONNECTION_PARAMS)

# Create a cursor object
cur = con.cursor()

# SQL statements for creating tables
sql_create_table_airportdimension = """
CREATE TABLE AIRPORTDIMENSION (
    "AIRPORT ID" INTEGER NOT NULL,
    "AIRPORT CODE" VARCHAR(3),
    "AIRPORT NAME" VARCHAR(100),
    CITY VARCHAR(100),
    STATE VARCHAR(100),
    LATITUDE NUMBER,
    LONGITUDE NUMBER,
    CHECKPOINT VARCHAR(50),
    CONSTRAINT "PK AIRPORTDIMENSION" PRIMARY KEY ("AIRPORT ID")
)
"""

sql_create_table_datedimensions = """
CREATE TABLE DATEDIMENSIONS (
    "HOUR DATE ID" INTEGER NOT NULL,
    DATE DATE,
    "HOUR OF DAY" DATETIME,
    "DAY OF WEEK" VARCHAR(10),
    MONTH VARCHAR(10),
    YEAR INTEGER,
    CONSTRAINT "PK ENTITY" PRIMARY KEY ("HOUR DATE ID")
)
"""

sql_create_table_facttable = """
CREATE TABLE FACTTABLE (
    "FACT ID" INTEGER NOT NULL,
    TEMPERATURE NUMBER,
    HUMIDITY NUMBER,
    "APPARENT TEMPERATURE" NUMBER,
    "PRECIPITATION RAIN" NUMBER,
    RAIN NUMBER,
    SNOWFALL NUMBER,
    "SNOW DEPTH" NUMBER,
    "CLOUD COVER TOTAL" NUMBER,
    "WIND SPEED" NUMBER,
    "WIND DIRECTION" VARCHAR(20),
    "HOUR DATE ID" INTEGER NOT NULL,
    "AIRPORT ID" INTEGER NOT NULL,
    "TOTAL PAX" NUMERIC,
    CONSTRAINT "PK FACTTABLE" PRIMARY KEY ("FACT ID", "HOUR DATE ID", "AIRPORT ID"),
    CONSTRAINT "FK FACTTABLE DATEDIMENSIONS" FOREIGN KEY ("HOUR DATE ID") REFERENCES DATEDIMENSIONS("HOUR DATE ID"),
    CONSTRAINT "FK FACTTABLE AIRPORTDIMENSION" FOREIGN KEY ("AIRPORT ID") REFERENCES AIRPORTDIMENSION("AIRPORT ID")
)
"""

# Execute the SQL commands
cur.execute(sql_create_table_airportdimension)
cur.execute(sql_create_table_datedimensions)
cur.execute(sql_create_table_facttable)

# Close the cursor and connection
cur.close()
con.close()
