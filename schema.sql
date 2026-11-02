CREATE DATABASE IF NOT EXISTS road_accident_db CHARACTER SET utf8mb4;
USE road_accident_db;
CREATE TABLE IF NOT EXISTS locations (
 location_id INT AUTO_INCREMENT PRIMARY KEY,
 region VARCHAR(120) NOT NULL,
 road_name VARCHAR(180) NULL,
 UNIQUE KEY uq_location (region, road_name)
);
CREATE TABLE IF NOT EXISTS accidents (
 accident_id INT AUTO_INCREMENT PRIMARY KEY,
 accident_datetime DATETIME NOT NULL,
 location_id INT NOT NULL,
 vehicle_type VARCHAR(60) NOT NULL,
 severity ENUM('Minor','Serious','Fatal','Unknown') NOT NULL DEFAULT 'Unknown',
 weather VARCHAR(60) NULL,
 source VARCHAR(255) NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (location_id) REFERENCES locations(location_id),
 INDEX idx_datetime (accident_datetime)
);
