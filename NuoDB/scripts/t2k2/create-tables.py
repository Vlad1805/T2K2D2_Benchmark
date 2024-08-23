import docker
import os

client = docker.from_env()

container_name = "t2k2-nuoadmin1-1"
sql_schema = "tmp/tables.sql"

container = client.containers.get(container_name)

sqlcmd_command = f"nuosql --user dba --password goalie hockey --file {sql_schema}"
exec_id = container.client.api.exec_create(container.id, f'/bin/sh -c "{sqlcmd_command}"')
output = container.client.api.exec_start(exec_id)
exit_code = container.client.api.exec_inspect(exec_id)['ExitCode']

if exit_code == 0:
    print("SQL script executed successfully:")
    print(output.decode('utf-8'))
else:
    print(f"Error executing SQL script: {output.decode('utf-8')}")

print("Process completed.")