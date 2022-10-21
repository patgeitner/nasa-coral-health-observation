createdb -h localhost -p 5432 -U postgres GOTECH
psql -d GOTECH -U postgres -c "CREATE EXTENSION postgis";