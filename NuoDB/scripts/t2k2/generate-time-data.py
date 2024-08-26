import docker
import os
import time 

client = docker.from_env()

container_name = "t2k2d2-nuoadmin1-1"
sql_schema = "tmp/tables.sql"
data_set = input("Enter the data set (500K, 1000K, 1500K, 2000K, 2500K): ")

container = client.containers.get(container_name)
sqlcmd_command_template = f"nuosql --user dba --password goalie hockey --timer full --file "
file_list = [
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q1_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q1_1w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q1_2w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q1_2w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q1_3w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q1_3w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q2_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q2_1w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q2_2w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q2_2w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q2_3w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q2_3w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q3_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q3_1w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q3_2w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q3_2w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q3_3w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q3_3w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q4_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q4_1w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q4_2w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q4_2w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q4_3w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_Okapi/Q4_3w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q1_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q1_1w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q1_2w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q1_2w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q1_3w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q1_3w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q2_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q2_1w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q2_2w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q2_2w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q2_3w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q2_3w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q3_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q3_1w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q3_2w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q3_2w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q3_3w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q3_3w_male.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q4_1w_female.sql",
    "/tmp/TopK_Documents/DB_NuoDB_TFIDF/Q4_1w_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q1_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q1_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q2_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q2_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q3_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q3_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q4_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_Okapi/Q4_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q1_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q1_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q2_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q2_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q3_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q3_male.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q4_female.sql",
    "/tmp/TopK_keywords/DB_NuoDB_TFIDF/Q4_male.sql"
]

directories = [
    "./logs/TopK_keywords/OLAP_NuoDB_TFIDF/",
    "./logs/TopK_keywords/OLAP_NuoDB_Okapi/",
    "./logs/TopK_Documents/OLAP_NuoDB_TFIDF/",
    "./logs/TopK_Documents/OLAP_NuoDB_Okapi/"
]

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

for file in file_list:
    sql_command = sqlcmd_command_template + file
    output_file = file.replace("/tmp/", "") + f"-{data_set}"
    print(f"Running command: {sql_command}")
    with open(f"./logs/{output_file}.log", "w") as f:
        for i in range(10):
            try:
                start_time = time.time()
                exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sql_command}"')
                output = container.client.api.exec_start(exec_id)
                exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']
                end_time = time.time()
                execution_time = end_time - start_time
                # Write execution time to file locate in /log/file-i.txt
                f.write(f"Execution time for command: {execution_time:.2f} seconds\n")
            except Exception as e:
                print(f"Error running command: {sql_command}")
                print(e)

print("Done!")
