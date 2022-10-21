psql -d GOTECH -U postgres -c "DROP TABLE IF EXISTS IceSat2;";
psql -d GOTECH -U postgres -c "CREATE TABLE IceSat2(
													height DECIMAL, 
													geo geography(POINT),
													date DATE);";

psql -d GOTECH -U postgres -c "DROP TABLE IF EXISTS Calipso;";
psql -d GOTECH -U postgres -c "CREATE TABLE Calipso(
													height DECIMAL, 
													geo geography(POINT));";

psql -d GOTECH -U postgres -c "DROP TABLE IF EXISTS Modis;";
psql -d GOTECH -U postgres -c "CREATE TABLE Modis(
												  latitude DECIMAL,
												  longitude DECIMAL,
												  chlor_a DECIMAL,
												  start_timestamp TIMESTAMP,
												  end_timestamp TIMESTAMP);";

psql -d GOTECH -U postgres -c "DROP TABLE IF EXISTS Landsat;";
psql -d GOTECH -U postgres -c "CREATE TABLE Landsat(
												  latitude DECIMAL,
												  longitude DECIMAL,
												  chlor_a DECIMAL,
												  start_timestamp TIMESTAMP,
												  end_timestamp TIMESTAMP);";