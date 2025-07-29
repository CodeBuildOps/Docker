FROM postgres:15

# Copy SQL script to the special init directory
COPY init.sql /docker-entrypoint-initdb.d/

# pg_isready: Checks if the database server is accepting connections
# Uses default postgres user
HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD pg_isready -U postgres || exit 1