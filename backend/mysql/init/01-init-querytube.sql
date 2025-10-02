-- QueryTube MySQL Database Initialization Script

-- Create the querytube database if it doesn't exist
CREATE DATABASE IF NOT EXISTS querytube CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user for QueryTube
CREATE USER IF NOT EXISTS 'querytube_user'@'%' IDENTIFIED BY 'querytube_password';

-- Grant permissions to the querytube user
GRANT ALL PRIVILEGES ON querytube.* TO 'querytube_user'@'%';

-- Grant permissions for local connections
GRANT ALL PRIVILEGES ON querytube.* TO 'querytube_user'@'localhost';

-- Flush privileges to ensure they take effect
FLUSH PRIVILEGES;

-- Switch to the querytube database
USE querytube;

-- Create indexes for better performance
-- Note: Tables will be created by SQLAlchemy, but we can add additional indexes here

-- Optimize MySQL settings for QueryTube
SET GLOBAL innodb_buffer_pool_size = 268435456; -- 256MB
SET GLOBAL max_connections = 200;
SET GLOBAL query_cache_size = 67108864; -- 64MB

-- Show success message
SELECT 'QueryTube MySQL database initialized successfully!' AS message;