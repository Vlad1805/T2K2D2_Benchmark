import ijson
import csv
from collections import defaultdict
import argparse
from datetime import datetime

# File paths (you can adjust these as needed)
json_file = '../../SetDate/'
genders_csv = 'genders.csv'
authors_csv = 'authors.csv'
geo_location_csv = 'geo_location.csv'
documents_csv = 'documents.csv'
words_csv = 'words.csv'
vocabulary_csv = 'vocabulary.csv'
documents_authors_csv = 'documents_authors.csv'

# Initialize IDs and data structures
gender_map = {'female': 1, 'male': 2}
word_map = {}
geo_location_id = 1
word_id = 1

geo_locations = {}
words = {}
vocabulary_entries = []
document_author_entries = []

# Create a parser object
parser = argparse.ArgumentParser(description="Script to validate a single argument.")

# Define the allowed choices for the argument
allowed_values = [
    "documents_clean500K.json",
    "documents_clean1000K.json",
    "documents_clean1500K.json",
    "documents_clean2000K.json",
    "documents_clean2500K.json"
]

# Add the argument with restricted choices and make it optional but required
parser.add_argument(
    "--json_file",
    choices=allowed_values,
    help="Specify the JSON file to use. Must be one of: --documents_clean500K.json, --documents_clean1000K.json, --documents_clean1500K.json, --documents_clean2000K.json, --documents_clean2500K.json"
)

# Parse the arguments
args = parser.parse_args()

if args.json_file == "documents_clean500K.json":
    print("You selected the 500K JSON file.")
    genders_csv = f"./csv/500K/{genders_csv}"
    authors_csv = f"./csv/500K/{authors_csv}"
    geo_location_csv = f"./csv/500K/{geo_location_csv}"
    documents_csv = f"./csv/500K/{documents_csv}"
    words_csv = f"./csv/500K/{words_csv}"
    vocabulary_csv = f"./csv/500K/{vocabulary_csv}"
    documents_authors_csv = f"./csv/500K/{documents_authors_csv}"
elif args.json_file == "documents_clean1000K.json":
    print("You selected the 1000K JSON file.")
    genders_csv = f"./csv/1000K/{genders_csv}"
    authors_csv = f"./csv/1000K/{authors_csv}"
    geo_location_csv = f"./csv/1000K/{geo_location_csv}"
    documents_csv = f"./csv/1000K/{documents_csv}"
    words_csv = f"./csv/1000K/{words_csv}"
    vocabulary_csv = f"./csv/1000K/{vocabulary_csv}"
    documents_authors_csv = f"./csv/1000K/{documents_authors_csv}"
elif args.json_file == "documents_clean1500K.json":
    print("You selected the 1500K JSON file.")
    genders_csv = f"./csv/1500K/{genders_csv}"
    authors_csv = f"./csv/1500K/{authors_csv}"
    geo_location_csv = f"./csv/1500K/{geo_location_csv}"
    documents_csv = f"./csv/1500K/{documents_csv}"
    words_csv = f"./csv/1500K/{words_csv}"
    vocabulary_csv = f"./csv/1500K/{vocabulary_csv}"
    documents_authors_csv = f"./csv/1500K/{documents_authors_csv}"
elif args.json_file == "documents_clean2000K.json":
    print("You selected the 2000K JSON file.")
    genders_csv = f"./csv/2000K/{genders_csv}"
    authors_csv = f"./csv/2000K/{authors_csv}"
    geo_location_csv = f"./csv/2000K/{geo_location_csv}"
    documents_csv = f"./csv/2000K/{documents_csv}"
    words_csv = f"./csv/2000K/{words_csv}"
    vocabulary_csv = f"./csv/2000K/{vocabulary_csv}"
    documents_authors_csv = f"./csv/2000K/{documents_authors_csv}"
elif args.json_file == "documents_clean2500K.json":
    print("You selected the 2500K JSON file.")
    genders_csv = f"./csv/2500K/{genders_csv}"
    authors_csv = f"./csv/2500K/{authors_csv}"
    geo_location_csv = f"./csv/2500K/{geo_location_csv}"
    documents_csv = f"./csv/2500K/{documents_csv}"
    words_csv = f"./csv/2500K/{words_csv}"
    vocabulary_csv = f"./csv/2500K/{vocabulary_csv}"
    documents_authors_csv = f"./csv/2500K/{documents_authors_csv}"
else:
    print("Invalid JSON file selected.")
    exit()

json_file = f"{json_file}{args.json_file}"

# Function to convert ISO 8601 date format to 'YYYY-MM-DD HH:MM:SS'
def convert_date_format(date_str):
    try:
        # Parse the ISO 8601 date
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Return the date in the format 'YYYY-MM-DD HH:MM:SS'
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"Error converting date: {e}")
        return None

def extract_author_id(author_field):
    """Extracts the author ID from the JSON entry, handling both $numberLong and direct integer cases."""
    if isinstance(author_field, dict) and '$numberLong' in author_field:
        return int(author_field['$numberLong'])
    elif isinstance(author_field, int):
        return author_field
    else:
        raise ValueError("Unexpected author format: {}".format(author_field))

# Open CSV files for writing
with open(genders_csv, 'w', newline='') as genders_file, \
     open(authors_csv, 'w', newline='') as authors_file, \
     open(geo_location_csv, 'w', newline='') as geo_location_file, \
     open(documents_csv, 'w', newline='') as documents_file, \
     open(words_csv, 'w', newline='') as words_file, \
     open(vocabulary_csv, 'w', newline='') as vocabulary_file, \
     open(documents_authors_csv, 'w', newline='') as documents_authors_file:

    # CSV writers
    genders_writer = csv.writer(genders_file)
    authors_writer = csv.writer(authors_file)
    geo_location_writer = csv.writer(geo_location_file)
    documents_writer = csv.writer(documents_file)
    words_writer = csv.writer(words_file)
    vocabulary_writer = csv.writer(vocabulary_file)
    documents_authors_writer = csv.writer(documents_authors_file)

    # Write gender data
    genders_writer.writerow([1, 'female'])
    genders_writer.writerow([2, 'male'])

    # Read JSON data in chunks to handle large file
    with open(json_file, 'r') as f:
        for entry in ijson.items(f, '', multiple_values=True):

            # Extract gender and author information
            gender = entry.get('gender')
            gender_id = gender_map.get(gender)

            try:
                author_id = extract_author_id(entry.get('author'))
            except ValueError as e:
                print(f"Skipping entry due to error: {e}")
                continue

            age = entry.get('age')

            # Write to authors table
            authors_writer.writerow([author_id, gender_id, '', '', age])

            # Extract geo location
            geoLocation = tuple(entry.get('geoLocation'))
            if geoLocation not in geo_locations:
                geo_locations[geoLocation] = geo_location_id
                geo_location_writer.writerow([geo_location_id, geoLocation[0], geoLocation[1]])
                geo_location_id += 1

            # Extract document data
            document_id = entry.get('_id', {}).get('$numberLong', entry.get('_id'))
            raw_text = entry.get('rawText')
            lemma_text = entry.get('lemmaText')
            clean_text = entry.get('cleanText')
            # Extract and convert the document date
            document_date_raw = entry.get('date', {}).get('$date')
            document_date = convert_date_format(document_date_raw)

            if document_date is None:
                print(f"Skipping entry due to date conversion error: {entry}")
                continue

            documents_writer.writerow([document_id, geo_locations[geoLocation], raw_text, lemma_text, clean_text, document_date])

            # Link author and document
            document_author_entries.append((author_id, document_id))

            # Process words and create vocabulary entries
            for word_entry in entry.get('words', []):
                word = word_entry.get('word')
                count = word_entry.get('count', 1)
                tf = word_entry.get('tf', 1.0)

                if word not in word_map:
                    word_map[word] = word_id
                    words_writer.writerow([word_id, word])
                    word_id += 1

                vocabulary_entries.append((document_id, word_map[word], count, tf))

        # Write all vocabulary and document-author data at once
        for entry in vocabulary_entries:
            vocabulary_writer.writerow(entry)

        for entry in document_author_entries:
            documents_authors_writer.writerow(entry)

print("CSV files have been generated successfully.")
