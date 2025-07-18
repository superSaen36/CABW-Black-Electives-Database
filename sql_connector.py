import sqlite3
from sheet_reader import ElectedOfficial, read_csv_as_objects
import csv

conn = sqlite3.connect("elected_officials.db")
cursor = conn.cursor()

# Define the schema
schema = """
CREATE TABLE elected_officials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    County TEXT,
    City TEXT,
    Office TEXT,
    District TEXT,
    Zip_Codes TEXT,
    Term_Length TEXT,
    Term_Expires TEXT,
    Term_Limits TEXT,
    Previous_Elected_Office TEXT,
    CABWC_PAC_Endorsed TEXT,
    Political_Party TEXT,
    Contact TEXT
);
"""

def add_csv_data():
    # Path to the CSV file
    csv_file_path = "/Users/seanbrown/project/cabw-elective-database/black-electeds-2023-2024-electeds.csv"
    # Insert data from the CSV file into the database
    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Replace empty values with None
            row = {key: (value if value.strip() else None) for key, value in row.items()}
            print(row)
            cursor.execute("""
                INSERT INTO elected_officials (
                    Name, County, City, Office, District, Zip_Codes, Term_Length, Term_Expires, Term_Limits,
                    Previous_Elected_Office, CABWC_PAC_Endorsed, Political_Party, Contact
                ) VALUES (
                    :Name, :County, :City, :Office, :District, :Zip_Codes, :Term_Length, :Term_Expires, :Term_Limits,
                    :Previous_Elected_Office, :CABWC_PAC_Endorsed, :Political_Party, :Contact
                )
            """, {
                "Name": row["Name"],
                "County": row["County"],
                "City": row["City"],
                "Office": row["Office"],
                "District": row["District"],
                "Zip_Codes": row["Zip Codes"],
                "Term_Length": row["Term Length"],
                "Term_Expires": row["Term Expires"],
                "Term_Limits": row["Term Limits"],
                "Previous_Elected_Office": row["Previous Elected Office"],
                "CABWC_PAC_Endorsed": row["CABWC PAC Endorsed"],
                "Political_Party": row["Polictical Party"],
                "Contact": row["Contact"]
            })

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Data inserted successfully!")

add_csv_data()