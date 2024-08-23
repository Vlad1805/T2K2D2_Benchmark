import docker
import os

# Initialize the Docker client
client = docker.from_env()

# Define the container name and CSV file paths
container_name = "t2k2-nuoadmin1-1"
gender_csv = "tmp/genders.csv"
author_csv = "tmp/authors.csv"
documents_csv = "tmp/documents.csv"
documents_authors_csv = "tmp/documents_authors.csv"
geo_location_csv = "tmp/geo_location.csv"
vocabulary_csv = "tmp/vocabulary.csv"
words_csv = "tmp/words.csv"

# Get the container by name
container = client.containers.get(container_name)

# Function to execute the nuoloader command in the Docker container
def execute_sql_command(container, sqlcmd_command):
    print(f"Executing: {sqlcmd_command}")
    
    # Create and execute the command inside the container
    exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sqlcmd_command}"')
    output = container.client.api.exec_start(exec_id)
    exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']
    
    # Check the exit code and print appropriate messages
    if exit_code == 0:
        print("SQL script executed successfully:")
        print(output.decode('utf-8'))
    else:
        print(f"Error executing SQL script: {output.decode('utf-8')}")
    
    return exit_code

# List of SQL commands to execute
commands = [
    f"nuoloader hockey --schema user --user dba --password goalie --import /tmp/genders.csv --to 'insert into genders values (?,?)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import /tmp/authors.csv --to 'insert into authors values (?,?,?,?,?)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import /tmp/documents.csv --to 'insert into documents values (?,?,?,?,?,?)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import /tmp/documents_authors.csv --to 'insert into documents_authors values (?,?)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import /tmp/geo_location.csv --to 'insert into geo_location values (?,?,?)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import /tmp/vocabulary.csv --to 'insert into vocabulary values (?,?,?,?)'",
    f"nuoloader hockey --schema user --user dba --password goalie --import /tmp/words.csv --to 'insert into words values (?,?)'"
]

# Execute each command and handle errors
for command in commands:
    exit_code = execute_sql_command(container, command)
    if exit_code != 0:
        print("Stopping execution due to an error.")
        break

print("Process completed.")
