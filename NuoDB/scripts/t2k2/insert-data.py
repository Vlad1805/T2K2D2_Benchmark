import docker
import os
import time  # Import the time module to measure execution time
import argparse

# Initialize the Docker client
client = docker.from_env()

# Define the container name and CSV file paths
container_name = "t2k2-nuoadmin1-1"
gender_csv = "genders.csv"
author_csv = "authors.csv"
documents_csv = "documents.csv"
documents_authors_csv = "documents_authors.csv"
geo_location_csv = "geo_location.csv"
vocabulary_csv = "vocabulary.csv"
words_csv = "words.csv"

# Get the container by name
container = client.containers.get(container_name)

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
    gender_csv = f"/tmp/csv/500K/{gender_csv}"
    author_csv = f"/tmp/csv/500K/{author_csv}"
    geo_location_csv = f"/tmp/csv/500K/{geo_location_csv}"
    documents_csv = f"/tmp/csv/500K/{documents_csv}"
    words_csv = f"/tmp/csv/500K/{words_csv}"
    vocabulary_csv = f"/tmp/csv/500K/{vocabulary_csv}"
    documents_authors_csv = f"/tmp/csv/500K/{documents_authors_csv}"
elif args.json_file == "documents_clean1000K.json":
    print("You selected the 1000K JSON file.")
    gender_csv = f"/tmp/csv/1000K/{gender_csv}"
    author_csv = f"/tmp/csv/1000K/{author_csv}"
    geo_location_csv = f"/tmp/csv/1000K/{geo_location_csv}"
    documents_csv = f"/tmp/csv/1000K/{documents_csv}"
    words_csv = f"/tmp/csv/1000K/{words_csv}"
    vocabulary_csv = f"/tmp/csv/1000K/{vocabulary_csv}"
    documents_authors_csv = f"/tmp/csv/1000K/{documents_authors_csv}"
elif args.json_file == "documents_clean1500K.json":
    print("You selected the 1500K JSON file.")
    gender_csv = f"/tmp/csv/1500K/{gender_csv}"
    author_csv = f"/tmp/csv/1500K/{author_csv}"
    geo_location_csv = f"/tmp/csv/1500K/{geo_location_csv}"
    documents_csv = f"/tmp/csv/1500K/{documents_csv}"
    words_csv = f"/tmp/csv/1500K/{words_csv}"
    vocabulary_csv = f"/tmp/csv/1500K/{vocabulary_csv}"
    documents_authors_csv = f"/tmp/csv/1500K/{documents_authors_csv}"
elif args.json_file == "documents_clean2000K.json":
    print("You selected the 2000K JSON file.")
    gender_csv = f"/tmp/csv/2000K/{gender_csv}"
    author_csv = f"/tmp/csv/2000K/{author_csv}"
    geo_location_csv = f"/tmp/csv/2000K/{geo_location_csv}"
    documents_csv = f"/tmp/csv/2000K/{documents_csv}"
    words_csv = f"/tmp/csv/2000K/{words_csv}"
    vocabulary_csv = f"/tmp/csv/2000K/{vocabulary_csv}"
    documents_authors_csv = f"/tmp/csv/{documents_authors_csv}"
elif args.json_file == "documents_clean2500K.json":
    print("You selected the 2500K JSON file.")
    gender_csv = f"/tmp/csv/2500K/{gender_csv}"
    author_csv = f"/tmp/csv/2500K/{author_csv}"
    geo_location_csv = f"/tmp/csv/2500K/{geo_location_csv}"
    documents_csv = f"/tmp/csv/2500K/{documents_csv}"
    words_csv = f"/tmp/csv/2500K/{words_csv}"
    vocabulary_csv = f"/tmp/csv/2500K/{vocabulary_csv}"
    documents_authors_csv = f"/tmp/csv/2500K/{documents_authors_csv}"
else:
    print("Invalid JSON file selected.")
    exit()

# Function to execute the nuoloader command in the Docker container
def execute_sql_command(container, sqlcmd_command):
    print(f"Executing: {sqlcmd_command}")
    
    # Record the start time for the command
    start_time = time.time()
    
    # Create and execute the command inside the container
    exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sqlcmd_command}"')
    output = container.client.api.exec_start(exec_id)
    exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']
    
    # Calculate and display the execution time for the command
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for command: {execution_time:.2f} seconds")
    
    # Check the exit code and print appropriate messages
    if exit_code == 0:
        print("SQL script executed successfully:")
        print(output.decode('utf-8'))
    else:
        print(f"Error executing SQL script: {output.decode('utf-8')}")
    
    return exit_code

# Record the start time for the entire script
script_start_time = time.time()

# List of SQL commands to execute
commands = [
    f"nuoloader hockey --schema user --user dba --password goalie --import {gender_csv} --to 'insert into genders values (?,?) ON DUPLICATE KEY UPDATE type=VALUES(type)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {author_csv} --to 'insert into authors values (?,?,?,?,?) ON DUPLICATE KEY UPDATE id_gender=VALUES(id_gender), firstname=VALUES(firstname), lastname=VALUES(lastname), age=VALUES(age)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {documents_csv} --to 'insert into documents values (?,?,?,?,?,?) ON DUPLICATE KEY UPDATE id_geo_loc=VALUES(id_geo_loc), raw_text=VALUES(raw_text), lemma_text=VALUES(lemma_text), clean_text=VALUES(clean_text), document_date=VALUES(document_date)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {documents_authors_csv} --to 'insert into documents_authors values (?,?) ON DUPLICATE KEY UPDATE id_author=VALUES(id_author), id_document=VALUES(id_document)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {geo_location_csv} --to 'insert into geo_location values (?,?,?) ON DUPLICATE KEY UPDATE X=VALUES(X), Y=VALUES(Y)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {vocabulary_csv} --to 'insert into vocabulary values (?,?,?,?) ON DUPLICATE KEY UPDATE count=VALUES(count), tf=VALUES(tf)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {words_csv} --to 'insert into words values (?,?) ON DUPLICATE KEY UPDATE word=VALUES(word)'"
]


# Execute each command and handle errors
for command in commands:
    exit_code = execute_sql_command(container, command)
    if exit_code != 0:
        print("Stopping execution due to an error.")
        break

# Record the end time for the entire script
script_end_time = time.time()

# Calculate and display the total execution time for the entire script
total_execution_time = script_end_time - script_start_time
print(f"Total execution time: {total_execution_time:.2f} seconds")

print("Process completed.")
