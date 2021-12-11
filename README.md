# Odoo Docker Hosting

## 1. Hosting Odoo with Docker 

> ### 1. Se connecter sur le serveur en ```SSH```
```bash 
-$ ssh <username>@192.162.70.149
```
> ### 2. Installer [docker](https://docs.docker.com/engine/install/ubuntu/)
> ### 3. installer [docker-compose](https://docs.docker.com/compose/install/) 
> ### 4. Creer un dossier ```src``` (endroit au choix)
```bash
-$ mkdir src
```
> ### 5. Cloner les repos necessaires
> > * Se deplacer dans le dossier
```bash
-$ cd src
```
> > * Odoo community addons

> > Ce dossier contient les addons community qui seront copiés dans le dossier ```/mnt/extra-addons``` dans le conteneur odoo
```bash
/src-$ git clone git@github.com:exonus/community-addons.git
```
> > * Exonus Databse Backup
> > Ce dossier contient les ```databases posgres``` exportées (sur l'instance ```bitnami``` qui tournait sur Azure)
> 
```bash
/src-$ git clone git@github.com:exonus/database-backup.git
```
> > * Odoo Docker Hosting
> > Ce dossier contient le projet ```docker-compose``` pour la construction des services ```Odoo``` et ```Postgres``` 

```bash
/src-$ git clone git@github.com:exonus/odoo-docker-hosting.git
```
> > * Vue du dossier ```src```
```
├── src
│   ├── community-addons
│   ├── database-backup
│   ├── odoo-docker-hosting

```
> ### 6. Les configurations CPU-RAM pour une bonne éxécution

```yaml
version: '3.1'
services:
  web:
    image: ...
    container_name: ...

    ...

    # directives
    deploy:
        resources:
            limits:
                cpus: '0.50'    # Le maximum utilisable par core (50%)
                memory: 2048M   # Le maximum utilisable dans la Ram (2Go)
            reservations:
                cpus: '0.25'    # Le minimum dedié par core (25%)
                memory: 512M    # Le minumum dedi2 dans la Ram (512Mo)
```

> ### 7. Demarrer les services ```odoo``` et ```postgres```

> > * Se deplacer dans le dossier ```odoo-docker-hosting```
```bash
/src-$ cd odoo-docker-hosting
```
> > * executer le fichier ```docker-compose.yml```
```bash
/src/odoo-docker-hosting-$ docker-compose up -d
```

> ### 7. Voir le resultat
> > * En local [localhost](localhost:80)
> > * En ligne [www.exonus.tech](http://www.exonus.tech/)


## 2. Restorer une databse Odoo dans un conteneur
> ### 1. Creer un user ```postgres``` 
```bash
-$ docker exec -i postgres_14 createuser -U bn_odoo postgres --superuser
```

> ### 2. Creer database ```bitnami_odoo```
```bash
-$ docker exec -i postgres_14 createdb -U bn_odoo bitnami_odoo
```

> ### 3. Restorer la database ```bitnami_odoo```
```bash
-$ docker exec -i postgres_14 psql -U bn_odoo bitnami_odoo < ../database-backup/bitnami_odoo.pgsql
```

> ### 4. Modifier le docker-compose pour utiliser la database ```bitnami_odoo```
```yaml
version: '3.1'
services:
  web:
    image: odoo:15.0
    container_name: odoo_15

    ...
    # updated line
    command: '-u all -d bitnami_odoo'
```

> ### 5. Run Odoo with database ```bitnami_odoo```
```bash
-$ docker-compose up -d
```

