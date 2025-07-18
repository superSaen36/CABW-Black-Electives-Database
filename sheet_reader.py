import csv
import sqlite3

# Define a class to represent each elected official
class ElectedOfficial:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"ElectedOfficial({self.__dict__})"
    

# Function to read the CSV file and store data as objects
def read_csv_as_objects(filepath):
    elected_officials = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create an ElectedOfficial object for each row
            official = ElectedOfficial(**row)
            elected_officials.append(official)
    return elected_officials

# Example usage
if __name__ == "__main__":
    filepath = "/Users/seanbrown/project/cabw-elective-database/Black Electeds 2023-2024.xlsx - Electeds.csv"
    officials = read_csv_as_objects(filepath)
    
    # # Print the first few objects to verify
    for official in officials[:5]:
        print(official.__dict__.keys())