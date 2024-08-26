import docker
import os
import time 

client = docker.from_env()

container_name = "t2k2d2-nuoadmin1-1"
sql_schema = "tmp/tables.sql"

container = client.containers.get(container_name)

start_time = time.time()

file_dict = {
    "1": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_1w_female.sql",
    "2": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_1w_male.sql",
    "3": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_2w_female.sql",
    "4": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_2w_male.sql",
    "5": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_3w_female.sql",
    "6": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q1_3w_male.sql",
    "7": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_1w_female.sql",
    "8": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_1w_male.sql",
    "9": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_2w_female.sql",
    "10": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_2w_male.sql",
    "11": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_3w_female.sql",
    "12": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q2_3w_male.sql",
    "13": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_1w_female.sql",
    "14": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_1w_male.sql",
    "15": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_2w_female.sql",
    "16": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_2w_male.sql",
    "17": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_3w_female.sql",
    "18": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q3_3w_male.sql",
    "19": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_1w_female.sql",
    "20": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_1w_male.sql",
    "21": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_2w_female.sql",
    "22": "/tmp/TopK_Documents/OLAP_NuoDB_Okapi/Q4_2w_male.sql",
    "23": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_1w_female.sql",
    "24": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_1w_male.sql",
    "25": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_2w_female.sql",
    "26": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_2w_male.sql",
    "27": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_3w_female.sql",
    "28": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q1_3w_male.sql",
    "29": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_1w_female.sql",
    "30": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_1w_male.sql",
    "31": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_2w_female.sql",
    "32": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q2_2w_male.sql",
    "33": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_1w_female.sql",
    "34": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_1w_male.sql",
    "35": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_2w_female.sql",
    "36": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q3_2w_male.sql",
    "37": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_1w_female.sql",
    "38": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_1w_male.sql",
    "39": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_2w_female.sql",
    "40": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_2w_male.sql",
    "41": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_3w_female.sql",
    "42": "/tmp/TopK_Documents/OLAP_NuoDB_TFIDF/Q4_3w_male.sql",
    "43": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q1_female.sql",
    "44": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q1_male.sql",
    "45": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q2_female.sql",
    "46": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q2_male.sql",
    "47": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q3_female.sql",
    "48": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q3_male.sql",
    "49": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q4_female.sql",
    "50": "/tmp/TopK_keywords/OLAP_NuoDB_Okapi/Q4_male.sql",
    "51": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q1_female.sql",
    "52": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q1_male.sql",
    "53": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q2_female.sql",
    "54": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q2_male.sql",
    "55": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q3_female.sql",
    "56": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q3_male.sql",
    "57": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q4_female.sql",
    "58": "/tmp/TopK_keywords/OLAP_NuoDB_TFIDF/Q4_male.sql"
}

id = input("Enter the ID of the SQL script to execute: ")
sqlcmd_command = f"nuosql --user dba --password goalie hockey --timer full --file {file_dict[id]}"
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