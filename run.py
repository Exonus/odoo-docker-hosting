# -*- coding:utf-8 -*-

import os
import sys
from typing import Container
import webbrowser
import time
# -*- coding:utf-8 -*-

import os
import sys
import webbrowser
import time


# services names
ODOO_SERVICE = "odoo_15"
POSTGRES_SERVICE = "postgres_14"

# current work directory path
cwd_path = os.getcwd()

# current work directory name
_, cwd_name = os.path.split(cwd_path)

def format_container_names():
    """Format containers names
    """

    # containers
    containers = []

    # add containers
    containers.append(f"{ODOO_SERVICE}")  # odoo container
    containers.append(f"{POSTGRES_SERVICE}")   # postgresql container

    return containers

def prune_volumes(all=False):
    volumes = [
        f"{cwd_name}_odoo-web-data", 
        f"{cwd_name}_odoo-db-data", 
        f"{cwd_name}_odoo-db-pgdata", 
    ]

    if all:
        for volume in volumes:
            os.system(f"docker volume rm {volume}")
            print(f"[Prune volume] '{volume}' success")
    
    # prune others
    os.system(f"docker volume prune")

def launch_odoo_in_browser():
    webbrowser.open_new_tab("localhost:8069/web?debug=1")

def create_db(container, db_user="bn_odoo", new_db="bitnami_odoo"):
    print(f"creation of database {new_db} starting")
    os.system(f"docker exec -i {container} createdb -U {db_user} {new_db}")
    print(f"creation of database {new_db} done")

def main():
    """Launch docker-compose services
    """

    # containers
    containers = format_container_names()

    # shutdown services and remove containers
    print("kill services and remove it")

    for container in containers:
        try:

            os.system(f"docker rm -f {container}")

        except Exception as error:
            print(f"[Error] : {error} ")

        else:
            print(
                f"[Success] : Container '{container}' shutdown and remove success")

    # set-up services

    try:

        # prune odoo volume
        if "--prune" in sys.argv:
            prune_volumes(all=True)

        os.system("docker-compose up -d")

        # create database
        create_db(
            container=ODOO_SERVICE,
        )

        

    except Exception as error:
        print(f"[Error] : {error}")

    else:
        os.system("docker ps")
        os.system("docker volume list")

        # open in browser
        print("Launch in browser")
        time.sleep(5)
        # launch_odoo_in_browser()


if __name__ == "__main__":
    main()