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

def run_mysql_container_docker(sql_script=None):
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
        "mysql:latest",
        environment=["MYSQL_ROOT_PASSWORD=test", "MYSQL_DATABASE=emedgene_v6", "MYSQL_USER=test", "MYSQL_PASSWORD=test"],
        ports={'3306/tcp': None},
        detach=True,
        volumes=volumes
    )

    # Wait for a few seconds to allow MySQL to initialize
    time.sleep(10)

    # Get the port
    container.reload()
    port = container.attrs['NetworkSettings']['Ports']['3306/tcp'][0]['HostPort']

    print(f"MySQL is running on localhost:{port}")

    return container

if __name__ == '__main__':
    script_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_mysql_container_docker(script_path)


