# Studienarbeit

## Start CassandraDB
```bash
1. Cassandra Image aus Docker Hub pullen:
docker pull cassandra:latest

2. Container starten:
docker run --name cassandra-secure -d -p 9042:9042 -e CASSANDRA_AUTHENTICATOR=PasswordAuthenticator -e CASSANDRA_USER=admin -e CASSANDRA_PASSWORD=admin123 cassandra

3. CQL-Shell starten:
docker exec -it cassandra cqlsh
```