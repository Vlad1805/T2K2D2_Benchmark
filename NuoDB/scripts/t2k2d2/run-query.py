import docker
import os
import time 

client = docker.from_env()

container_name = "t2k2d2-nuoadmin1-1"
sql_schema = "tmp/tables.sql"

container = client.containers.get(container_name)

start_time = time.time()

file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_3w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_3w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_3w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_3w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_3w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_3w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_3w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_3w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_1w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_1w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_2w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_2w_male.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_3w_female.sql"
file = "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_3w_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q1_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q1_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q2_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q2_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q3_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q3_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q4_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q4_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q1_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q1_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q2_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q2_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q3_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q3_male.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q4_female.sql"
file = "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q4_male.sql"

sqlcmd_command = f"nuosql --user dba --password goalie hockey --timer full --file {file}"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sqlcmd_command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time for command: {execution_time:.2f} seconds")
if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("Process completed.")