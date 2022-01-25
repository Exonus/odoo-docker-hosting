# Odoo Docker Hosting

## Déployer Odoo avec Docker 

### Préparer les sources sur le serveur
1. Se connecter sur le serveur en ```SSH```

   ```bash 
   $ ssh <username>@192.162.70.149
   ```
2. Installer [docker](https://docs.docker.com/engine/install/ubuntu/)
3. installer [docker-compose](https://docs.docker.com/compose/install/) 
4. Creer un dossier ```src``` (endroit au choix) et le visiter
   ```bash
   $ mkdir src
   $ cd src
   ```
5. Cloner les répos git
- Odoo community addons: Ce dossier contient les addons community qui seront copiés dans le dossier ```/mnt/extra-addons``` dans le conteneur odoo
- Exonus Databse Backup: Ce dossier contient les ```databases posgres``` exportées (sur l'instance ```bitnami``` qui tournait sur Azure)
- Odoo Docker Hosting: Ce dossier contient le projet ```docker-compose``` pour la construction des services ```Odoo``` et ```Postgres``` 

   ```bash
   /src-$ git clone git@github.com:exonus/community-addons.git
   /src-$ git clone git@github.com:exonus/database-backup.git
   /src-$ git clone git@github.com:exonus/odoo-docker-hosting.git
   ```

-  Vue du dossier ```src```
   ```
   ├── src
   │   ├── community-addons
   │   ├── database-backup
   │   ├── odoo-docker-hosting
   
   ```
6. Les configurations CPU-RAM pour une bonne éxécution

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

### Générer les certificats avec certbot

Depuis le répertoire `src/odoo-docker-hosting`, démarer `nginx` en vue de l'appel `certbot`: 

    ```
    docker-compose -f docker-compose-generate-certs.yml up -d
    ```

Puis, une fois que nginx roule, executer la commande suivante afin de tester la génération du certificat :

    ```
    docker-compose -f docker-compose-generate-certs.yml run --rm  certbot certonly --webroot --webroot-path /var/www/html/ --email nathanbangwa.exonus@gmail.com --agree-tos --no-eff-email --dry-run -d exonus.tech -d www.exonus.tech
    ```
Si tout est bon, on obtien un message du genre : 

    ```
    Simulating a certificate request for exonus.tech 
    The dry run was successful.
    ```
Alors on peut procéder à la génération du certificat (sans le `--dry-run`)

    ```
    docker-compose -f docker-compose-generate-certs.yml run --rm  certbot certonly --webroot --webroot-path /var/www/html/ --email nathanbangwa.exonus@gmail.com --agree-tos --no-eff-email -d exonus.tech -d www.exonus.tech
    ```
Une fois les certificats générés :

    ```
    docker-compose -f docker-compose-generate-certs.yml down
    ```
à partir d'ici, le fichier docker-compose `docker-compose-generate-certs.yml` ne sera plus utilisé (sauf pour effectuer le renouvellement des certificats).

### Demarrer les services ```odoo``` et ```postgres```

Se deplacer dans le dossier ```src/odoo-docker-hosting``` et executer le fichier ```docker-compose.yml``` en background ```-d```
   ```bash
   /src-$ cd odoo-docker-hosting
   /src/odoo-docker-hosting-$ docker-compose up -d
   ```

Voir le resultat
   - En local [localhost](http://localhost:80)
   - En ligne [www.exonus.tech](http://www.exonus.tech/)


## Restorer une databse Odoo dans un conteneur
Executer `docker-compose` en background ```-d```
```bash
/src/odoo-docker-hosting-$ docker-compose up -d
```
> ### 2. Creer un superuser ```postgres``` 
```bash
/src/odoo-docker-hosting-$ docker exec -i postgres_14 createuser -U bn_odoo postgres --superuser
```

> ### 3. Creer la database ```bitnami_odoo```
```bash
/src/odoo-docker-hosting-$ docker exec -i postgres_14 createdb -U bn_odoo bitnami_odoo
```

> ### 4. Restorer la database ```bitnami_odoo```
```bash
/src/odoo-docker-hosting-$ docker exec -i postgres_14 psql -U bn_odoo bitnami_odoo < ../database-backup/bitnami_odoo.pgsql
```

> ### 5. Modifier le docker-compose pour utiliser la database ```bitnami_odoo``` restaurée
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

> ### 6. executer le fichier ```docker-compose.yml``` en background ```-d```
```bash
/src/odoo-docker-hosting-$ docker-compose up -d
```
