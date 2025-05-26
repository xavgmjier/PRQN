from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from nanoid import generate


# ////// Create the database tables \\\\\\
connection = sqlite3.connect('InvestorCommitments.db')
connection.execute("PRAGMA foreign_keys = 1")
connection.execute('''
    CREATE TABLE IF NOT EXISTS investors
       (
            investor_id TEXT PRIMARY KEY,
            investor_name TEXT NOT NULL,
            investory_type TEXT NOT NULL, 
	        investor_country TEXT NOT NULL,
            investor_date_added TEXT NOT NULL,
            investor_last_updated TEXT NOT NULL
        );
''')

connection.execute('''
    CREATE TABLE IF NOT EXISTS commitments
       (
            commitment_id TEXT PRIMARY KEY,
            commitment_asset_class TEXT NOT NULL,
            commitment_amount INTEGER NOT NULL, 
	        commitment_currency TEXT NOT NULL,
            investor_id INTEGER NOT NULL,
            FOREIGN KEY (investor_id) REFERENCES investors (investor_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
''')
 
connection.close()

# ////// Create pandas dataframe from database tables \\\\\\

engine = create_engine('sqlite:///InvestorCommitments.db')
# Reading the SQLite table
investors_df = pd.read_sql('investors', engine)
commitments_df = pd.read_sql('commitments', engine)

# ////// Read data from original source csv \\\\\\
# Step 1 - Load csv file
source_df = pd.read_csv('./data.csv')

# Step 2 - Get columns from csv
source_df.columns = source_df.columns.str.strip()

# Step 3 - Create new columns to use as an eventual primaryKey and foreignKey in the database
# Generate a unique ID for each row in the Commitment ID column 
source_df.insert(0, 'Commitment ID', [generate(size=10) for _ in range(len(source_df))], False)

# Hash the investor name and date added to generate a unique ID for each investor
source_df.insert(0, 'Investor ID',\
    [str(abs(hash(source_df.iloc[x]['Investor Name'] + source_df.iloc[x]['Investor Date Added']))) for x in range(len(source_df))], False)


# Step 4 - Create new dataframes baed on the source, that match the structure of the previously created database tables 
investors_data_frame = source_df[['Investor ID','Investor Name',\
                                  'Investory Type','Investor Country',\
                                  'Investor Date Added', 'Investor Last Updated']]

commitments_data_frame = source_df[['Commitment ID', 'Commitment Asset Class',\
                                    'Commitment Amount', 'Commitment Currency',\
                                    'Investor ID']]


# Step 5 - Standardise column names for both dataframes - include underscore and make lowercase
investors_data_frame.columns = list(map(lambda c: c.lower().replace(' ', '_'), investors_data_frame.columns))
commitments_data_frame.columns = list(map(lambda c: c.lower().replace(' ', '_'), commitments_data_frame.columns))

# Step 6 - Remove duplicate rows within the investors dataframe
investors_data_frame_deduplicated = investors_data_frame.drop_duplicates(subset="investor_name")

# Step 7 - Merge (hydrate?) empty base dataframes with data containing ones
enriched_investors_df = pd.concat([investors_df, investors_data_frame_deduplicated], ignore_index=True)
enriched_commitments_df = pd.concat([commitments_df, commitments_data_frame], ignore_index=True)

# Step 8 - Write dataframe data to database tables
try:
    print("writing to database")
    enriched_investors_df.to_sql('investors', engine, if_exists='append', index=False)
    enriched_commitments_df.to_sql('commitments', engine, if_exists='append', index=False)
except Exception as e:
  print("Something went wrong while running the database build script: ", e)

engine.dispose()
