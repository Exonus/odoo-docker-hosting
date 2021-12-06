# odoo-docker-hosting

## Create user postgres 
docker exec -i postgres_14 createuser -U bn_odoo postgres --superuser

## Create database bitnami_odoo
docker exec -i postgres_14 createdb -U bn_odoo bitnami_odoo

## Restore database bitnami_odoo
docker exec -i postgres_14 psql -U bn_odoo bitnami_odoo < ../database-backup/bitnami_odoo.pgsql

