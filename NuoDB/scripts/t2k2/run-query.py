import docker
import os
import time 

client = docker.from_env()

container_name = "t2k2-nuoadmin1-1"
sql_schema = "tmp/tables.sql"

container = client.containers.get(container_name)

start_time = time.time()
sqlcmd_command = f"nuosql --user dba --password goalie hockey --file /tmp/DB_NuoDB_Okapi/Q1_1w_female.sql"
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