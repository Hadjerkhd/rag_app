-- Create an application user
CREATE USER appuser WITH PASSWORD 'apppassword';

-- Create the application database if not created by POSTGRES_DB
CREATE DATABASE researcher_assistantdb OWNER appuser;

-- Grant all permissions on appdb to appuser
GRANT ALL PRIVILEGES ON DATABASE researcher_assistantdb TO appuser;
