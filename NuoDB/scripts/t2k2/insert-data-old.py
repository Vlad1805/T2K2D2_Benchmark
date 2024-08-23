import ijson
import docker
import os

# Initialize Docker client
client = docker.from_env()

# Define container and SQL script details
container_name = "t2k2-nuoadmin1-1"
container = client.containers.get(container_name)

sql_file_path = "tmp/batch_inserts.sql"
host_sql_file_path = "batch_inserts.sql"
batch_size = 100

# Function to execute a SQL file using nuosql
def execute_sql_file():
    sqlcmd_command = f'nuosql --user dba --password goalie hockey --file {sql_file_path}'
    exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sqlcmd_command}"')
    output = container.client.api.exec_start(exec_id)
    exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']
    if exit_code != 0:
        raise RuntimeError(f"SQL command failed: {output.decode('utf-8')}")
    return output.decode('utf-8')

# Function to write SQL commands to the file
def write_sql_to_file(sql_commands):
    with open(host_sql_file_path, 'w') as sql_file:
        sql_file.write('\n'.join(sql_commands) + '\n')

# Path to the JSON file
json_file_path = "/Users/vstanciu/Desktop/Vlad/facultate/bd2/T2K2D2_Benchmark/NuoDB/SetDate/test.json"

sql_commands = []
command_count = 0

# Read and process each JSON object
with open(json_file_path, 'r') as file:
    for obj in ijson.items(file, '', multiple_values=True):
        # Extract data from JSON object
        doc_id = obj["_id"]["$numberLong"] if isinstance(obj["_id"], dict) else obj["_id"]
        raw_text = obj["rawText"].replace("'", "''")  # Escape single quotes
        clean_text = obj["cleanText"].replace("'", "''")
        lemma_text = obj["lemmaText"].replace("'", "''")
        document_date = obj["date"]["$date"]
        author_id = obj["author"]["$numberLong"] if isinstance(obj["author"], dict) else obj["author"]
        gender_type = obj["gender"]
        age = obj["age"]
        geo_location = obj["geoLocation"]
        words = obj["words"]


        # Create SQL commands
        gender_insert = (
            f"INSERT INTO genders (id, type) "
            f"VALUES ({author_id}, '{gender_type}') "
            f"ON DUPLICATE KEY UPDATE type=VALUES(type);"
        )
        sql_commands.append(gender_insert)

        author_insert = (
            f"INSERT INTO authors (id, id_gender, age) "
            f"VALUES ({author_id}, {author_id}, {age}) "
            f"ON DUPLICATE KEY UPDATE age=VALUES(age);"
        )
        sql_commands.append(author_insert)

        geo_insert = (
            f"INSERT INTO geo_location (id, X, Y) "
            f"VALUES ({doc_id}, {float(geo_location[0])}, {float(geo_location[1])}) "
            f"ON DUPLICATE KEY UPDATE X=VALUES(X), Y=VALUES(Y);"
        )
        sql_commands.append(geo_insert)

        document_insert = (
            f"INSERT INTO documents (id, id_geo_loc, raw_text, lemma_text, clean_text, document_date) "
            f"VALUES ({doc_id}, {doc_id}, {raw_text}, {lemma_text}, {clean_text}, {document_date}) "
            f"ON DUPLICATE KEY UPDATE raw_text=VALUES(raw_text), lemma_text=VALUES(lemma_text), clean_text=VALUES(clean_text), document_date=VALUES(document_date);"
        )
        sql_commands.append(document_insert)

        doc_author_insert = (
            f"INSERT INTO documents_authors (id_author, id_document) "
            f"VALUES ({author_id}, {doc_id}) "
            f"ON DUPLICATE KEY UPDATE id_author=VALUES(id_author), id_document=VALUES(id_document);"
        )
        sql_commands.append(doc_author_insert)

        for word_obj in words:
            word = word_obj["word"].replace("'", "''")
            count = word_obj["count"]
            tf = word_obj["tf"]

            word_insert = (
                f"INSERT INTO words (word) "
                f"VALUES ('{word}') "
                f"ON DUPLICATE KEY UPDATE word=VALUES(word);"
            )
            sql_commands.append(word_insert)

            vocabulary_insert = (
                f"INSERT INTO vocabulary (id_document, id_word, count, tf) "
                f"VALUES ({doc_id}, (SELECT id FROM words WHERE word='{word}'), {count}, {tf}) "
                f"ON DUPLICATE KEY UPDATE count=VALUES(count), tf=VALUES(tf);"
            )
            sql_commands.append(vocabulary_insert)

        # Increment the command count
        command_count += 1

        # Execute and reset after reaching the batch size
        if command_count >= batch_size:
            # Write SQL commands to file
            write_sql_to_file(sql_commands)
            # Execute the SQL file
            execute_sql_file()
            # Clear the SQL file and reset the command count
            sql_commands = []
            command_count = 0
        
        print(f"Processing document {type(geo_location[0])}...")
        print(document_insert)
        exit()

# Process any remaining commands after the loop ends
if sql_commands:
    write_sql_to_file(sql_commands)
    execute_sql_file()

print("Data insertion completed.")
