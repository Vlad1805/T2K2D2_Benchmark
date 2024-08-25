import docker
import os
import time  # Import the time module to measure execution time
import argparse

# Initialize the Docker client
client = docker.from_env()

# Define the container name and CSV file paths
container_name = "t2k2d2-nuoadmin1-1"
author_dimension_csv = "author_dimension.csv"
document_dimension_csv = "document_dimension.csv"
time_dimension_csv = "time_dimension.csv"
location_dimension_csv = "location_dimension.csv"
word_dimension_csv = "word_dimension.csv"
document_fact_csv = "document_fact.csv"

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
    author_dimension_csv = f"/tmp/csv/500K/{author_dimension_csv}"
    document_dimension_csv = f"/tmp/csv/500K/{document_dimension_csv}"
    word_dimension_csv = f"/tmp/csv/500K/{word_dimension_csv}"
    time_dimension_csv = f"/tmp/csv/500K/{time_dimension_csv}"
    document_fact_csv = f"/tmp/csv/500K/{document_fact_csv}"
    location_dimension_csv = f"/tmp/csv/500K/{location_dimension_csv}"
elif args.json_file == "documents_clean1000K.json":
    print("You selected the 1000K JSON file.")
    author_dimension_csv = f"/tmp/csv/1000K/{author_dimension_csv}"
    document_dimension_csv = f"/tmp/csv/1000K/{document_dimension_csv}"
    word_dimension_csv = f"/tmp/csv/1000K/{word_dimension_csv}"
    time_dimension_csv = f"/tmp/csv/1000K/{time_dimension_csv}"
    document_fact_csv = f"/tmp/csv/1000K/{document_fact_csv}"
    location_dimension_csv = f"/tmp/csv/1000K/{location_dimension_csv}"
elif args.json_file == "documents_clean1500K.json":
    print("You selected the 1500K JSON file.")
    author_dimension_csv = f"/tmp/csv/1500K/{author_dimension_csv}"
    document_dimension_csv = f"/tmp/csv/1500K/{document_dimension_csv}"
    word_dimension_csv = f"/tmp/csv/1500K/{word_dimension_csv}"
    time_dimension_csv = f"/tmp/csv/1500K/{time_dimension_csv}"
    document_fact_csv = f"/tmp/csv/1500K/{document_fact_csv}"
    location_dimension_csv = f"/tmp/csv/1500K/{location_dimension_csv}"
elif args.json_file == "documents_clean2000K.json":
    print("You selected the 2000K JSON file.")
    author_dimension_csv = f"/tmp/csv/2000K/{author_dimension_csv}"
    document_dimension_csv = f"/tmp/csv/2000K/{document_dimension_csv}"
    word_dimension_csv = f"/tmp/csv/2000K/{word_dimension_csv}"
    time_dimension_csv = f"/tmp/csv/2000K/{time_dimension_csv}"
    document_fact_csv = f"/tmp/csv/2000K/{document_fact_csv}"
    location_dimension_csv = f"/tmp/csv/{location_dimension_csv}"
elif args.json_file == "documents_clean2500K.json":
    print("You selected the 2500K JSON file.")
    author_dimension_csv = f"/tmp/csv/2500K/{author_dimension_csv}"
    document_dimension_csv = f"/tmp/csv/2500K/{document_dimension_csv}"
    word_dimension_csv = f"/tmp/csv/2500K/{word_dimension_csv}"
    time_dimension_csv = f"/tmp/csv/2500K/{time_dimension_csv}"
    document_fact_csv = f"/tmp/csv/2500K/{document_fact_csv}"
    location_dimension_csv = f"/tmp/csv/2500K/{location_dimension_csv}"
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
    f"nuoloader hockey --schema user --user dba --password goalie --import {author_dimension_csv} --to 'insert into author_dimension values (?,?,?,?,?) ON DUPLICATE KEY UPDATE firstname=VALUES(firstname), lastname=VALUES(lastname), gender=VALUES(gender), age=VALUES(age)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {document_dimension_csv} --to 'insert into document_dimension values (?,?,?,?) ON DUPLICATE KEY UPDATE raw_text=VALUES(raw_text), clean_text=VALUES(clean_text), lemma_text=VALUES(lemma_text)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {time_dimension_csv} --to 'insert into time_dimension values (?,?,?,?,?,?,?) ON DUPLICATE KEY UPDATE minute=VALUES(minute), hour=VALUES(hour), day=VALUES(day), month=VALUES(month), year=VALUES(year), full_date=VALUES(full_date)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {location_dimension_csv} --to 'insert into location_dimension values (?,?,?) ON DUPLICATE KEY UPDATE X=VALUES(X), Y=VALUES(Y)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {word_dimension_csv} --to 'insert into word_dimension values (?,?) ON DUPLICATE KEY UPDATE word=VALUES(word)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import {document_fact_csv} --to 'insert into document_fact values (?,?,?,?,?,?,?) ON DUPLICATE KEY UPDATE count=VALUES(count), tf=VALUES(tf)'",
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
