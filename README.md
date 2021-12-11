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
```bash
/src-$ git clone git@github.com:exonus/community-addons.git
```
> > * Exonus Databse Backup
```bash
/src-$ git clone git@github.com:exonus/database-backup.git
```
> > * Odoo Hocker Hosting
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

> ### 6. Demarrer les services ```odoo``` et ```postgres```

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


## 2. Restore Odoo Data into container
> ### 1. Create user postgres 
```bash
-$ docker exec -i postgres_14 createuser -U bn_odoo postgres --superuser
```

> ### 2. Create database bitnami_odoo
```bash
-$ docker exec -i postgres_14 createdb -U bn_odoo bitnami_odoo
```

> ### 3. Restore database ```bitnami_odoo```
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

