import ijson
import csv
from collections import defaultdict
import argparse
from datetime import datetime

# File paths (adjust these as needed)
json_file = '../../SetDate/'
document_dimension_csv = 'document_dimension.csv'
author_dimension_csv = 'author_dimension.csv'
time_dimension_csv = 'time_dimension.csv'
location_dimension_csv = 'location_dimension.csv'
word_dimension_csv = 'word_dimension.csv'
document_fact_csv = 'document_fact.csv'

# Initialize IDs and data structures
document_id = 1
author_id = 1
time_id = 1
location_id = 1
word_id = 1

documents = {}
authors = {}
times = {}
locations = {}
words = {}

document_facts = []

# Create a parser object
parser = argparse.ArgumentParser(description="Script to validate a single argument.")

# Define the allowed choices for the argument
allowed_values = [
    "documents_clean500K.json",
    "documents_clean1000K.json",
    "documents_clean1500K.json",
    "documents_clean2000K.json",
    "documents_clean2500K.json",
    "test.json",
]

# Add the argument with restricted choices and make it optional but required
parser.add_argument(
    "--json_file",
    choices=allowed_values,
    help="Specify the JSON file to use. Must be one of: --documents_clean500K.json, --documents_clean1000K.json, --documents_clean1500K.json, --documents_clean2000K.json, --documents_clean2500K.json, --test.json"
)

# Parse the arguments
args = parser.parse_args()

if args.json_file == "documents_clean500K.json":
    print("You selected the 500K JSON file.")
    document_dimension_csv = f"./csv/500K/{document_dimension_csv}"
    author_dimension_csv = f"./csv/500K/{author_dimension_csv}"
    time_dimension_csv = f"./csv/500K/{time_dimension_csv}"
    location_dimension_csv = f"./csv/500K/{location_dimension_csv}"
    word_dimension_csv = f"./csv/500K/{word_dimension_csv}"
    document_fact_csv = f"./csv/500K/{document_fact_csv}"
elif args.json_file == "documents_clean1000K.json":
    print("You selected the 1000K JSON file.")
    document_dimension_csv = f"./csv/1000K/{document_dimension_csv}"
    author_dimension_csv = f"./csv/1000K/{author_dimension_csv}"
    time_dimension_csv = f"./csv/1000K/{time_dimension_csv}"
    location_dimension_csv = f"./csv/1000K/{location_dimension_csv}"
    word_dimension_csv = f"./csv/1000K/{word_dimension_csv}"
    document_fact_csv = f"./csv/1000K/{document_fact_csv}"
elif args.json_file == "documents_clean1500K.json":
    print("You selected the 1500K JSON file.")
    document_dimension_csv = f"./csv/1500K/{document_dimension_csv}"
    author_dimension_csv = f"./csv/1500K/{author_dimension_csv}"
    time_dimension_csv = f"./csv/1500K/{time_dimension_csv}"
    location_dimension_csv = f"./csv/1500K/{location_dimension_csv}"
    word_dimension_csv = f"./csv/1500K/{word_dimension_csv}"
    document_fact_csv = f"./csv/1500K/{document_fact_csv}"
elif args.json_file == "documents_clean2000K.json":
    print("You selected the 2000K JSON file.")
    document_dimension_csv = f"./csv/2000K/{document_dimension_csv}"
    author_dimension_csv = f"./csv/2000K/{author_dimension_csv}"
    time_dimension_csv = f"./csv/2000K/{time_dimension_csv}"
    location_dimension_csv = f"./csv/2000K/{location_dimension_csv}"
    word_dimension_csv = f"./csv/2000K/{word_dimension_csv}"
    document_fact_csv = f"./csv/2000K/{document_fact_csv}"
elif args.json_file == "documents_clean2500K.json":
    print("You selected the 2500K JSON file.")
    document_dimension_csv = f"./csv/2500K/{document_dimension_csv}"
    author_dimension_csv = f"./csv/2500K/{author_dimension_csv}"
    time_dimension_csv = f"./csv/2500K/{time_dimension_csv}"
    location_dimension_csv = f"./csv/2500K/{location_dimension_csv}"
    word_dimension_csv = f"./csv/2500K/{word_dimension_csv}"
    document_fact_csv = f"./csv/2500K/{document_fact_csv}"
elif args.json_file == "test.json":
    print("You selected the test JSON file.")
    document_dimension_csv = f"./csv/test/{document_dimension_csv}"
    author_dimension_csv = f"./csv/test/{author_dimension_csv}"
    time_dimension_csv = f"./csv/test/{time_dimension_csv}"
    location_dimension_csv = f"./csv/test/{location_dimension_csv}"
    word_dimension_csv = f"./csv/test/{word_dimension_csv}"
    document_fact_csv = f"./csv/test/{document_fact_csv}"

json_file = f"{json_file}{args.json_file}"

def convert_date_to_time_dimension(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return {
        "minute": dt.minute,
        "hour": dt.hour,
        "day": dt.day,
        "month": dt.month,
        "year": dt.year,
        "full_date": dt.strftime("%Y-%m-%d %H:%M:%S")
    }

def extract_author_id(author_field):
    """Extracts the author ID from the JSON entry, handling both $numberLong and direct integer cases."""
    if isinstance(author_field, dict) and '$numberLong' in author_field:
        return int(author_field['$numberLong'])
    elif isinstance(author_field, int):
        return author_field
    else:
        raise ValueError("Unexpected author format: {}".format(author_field))

# Open CSV files for writing
with open(document_dimension_csv, 'w', newline='') as doc_dim_file, \
     open(author_dimension_csv, 'w', newline='') as author_dim_file, \
     open(time_dimension_csv, 'w', newline='') as time_dim_file, \
     open(location_dimension_csv, 'w', newline='') as loc_dim_file, \
     open(word_dimension_csv, 'w', newline='') as word_dim_file, \
     open(document_fact_csv, 'w', newline='') as doc_fact_file:

    # CSV writers
    doc_dim_writer = csv.writer(doc_dim_file)
    author_dim_writer = csv.writer(author_dim_file)
    time_dim_writer = csv.writer(time_dim_file)
    loc_dim_writer = csv.writer(loc_dim_file)
    word_dim_writer = csv.writer(word_dim_file)
    doc_fact_writer = csv.writer(doc_fact_file)

    # Read JSON data
    with open(json_file, 'r') as f:
        for entry in ijson.items(f, '', multiple_values=True):
            # Extract document data
            raw_text = entry.get('rawText')
            clean_text = entry.get('cleanText')
            lemma_text = entry.get('lemmaText')

            if (raw_text, clean_text, lemma_text) not in documents:
                documents[(raw_text, clean_text, lemma_text)] = document_id
                doc_dim_writer.writerow([document_id, raw_text, clean_text, lemma_text])
                document_id += 1

            doc_id = documents[(raw_text, clean_text, lemma_text)]

            # Extract author data
            author = extract_author_id(entry.get('author'))
            gender = entry.get('gender')
            age = entry.get('age')
            author_key = (author, gender, age)

            if author_key not in authors:
                authors[author_key] = author_id
                author_dim_writer.writerow([author_id, '', '', gender, age])
                author_id += 1

            auth_id = authors[author_key]

            # Extract time data
            document_date = entry.get('date', {}).get('$date')
            time_data = convert_date_to_time_dimension(document_date)

            time_key = (time_data['minute'], time_data['hour'], time_data['day'], time_data['month'], time_data['year'])
            if time_key not in times:
                times[time_key] = time_id
                time_dim_writer.writerow([time_id, time_data['minute'], time_data['hour'], time_data['day'], time_data['month'], time_data['year'], time_data['full_date']])
                time_id += 1

            time_id_ref = times[time_key]

            # Extract location data
            geo_location = tuple(entry.get('geoLocation'))
            if geo_location not in locations:
                locations[geo_location] = location_id
                loc_dim_writer.writerow([location_id, geo_location[0], geo_location[1]])
                location_id += 1

            loc_id = locations[geo_location]

            # Extract word data and create document_fact entries
            for word_entry in entry.get('words', []):
                word = word_entry.get('word')
                count = word_entry.get('count', 1)
                tf = word_entry.get('tf', 1.0)

                if word not in words:
                    words[word] = word_id
                    word_dim_writer.writerow([word_id, word])
                    word_id += 1

                word_id_ref = words[word]

                # Add document_fact entry
                doc_fact_writer.writerow([doc_id, auth_id, time_id_ref, loc_id, word_id_ref, count, tf])

print("CSV files generated successfully.")
