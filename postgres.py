import docker
import sys
import os
import time


"""
bash function to trigger this file
run_mysql_test_db() {
    python /path/to/run_mysql_test_db.py "$1"
}

"""

def run_postgres_container_docker(sql_script=None):
    client = docker.from_env()

    # Validate and prepare the SQL script path
    volumes = {}
    if sql_script:
        sql_script_path = os.path.abspath(sql_script)
        if not os.path.exists(sql_script_path):
            print(f"SQL script file does not exist: {sql_script_path}")
            return
        volumes = {sql_script_path: {'bind': '/docker-entrypoint-initdb.d/init.sql', 'mode': 'ro'}}

    container = client.containers.run(
        "postgres:latest",
        environment={"POSTGRES_PASSWORD": "test", "POSTGRES_DB": "emedgene_v6", "POSTGRES_USER": "test"},
        ports={'5432/tcp': None},
        detach=True,
        volumes=volumes
    )

    # Wait for a few seconds to allow PostgreSQL to initialize
    time.sleep(10)

    # Get the port
    container.reload()
    port = container.attrs['NetworkSettings']['Ports']['5432/tcp'][0]['HostPort']

    print(f"PostgreSQL is running on localhost:{port}")

    return container

if __name__ == '__main__':
    script_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_postgres_container_docker(script_path)



