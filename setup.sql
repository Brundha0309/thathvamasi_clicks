-- Run this in MySQL to create the database
CREATE DATABASE IF NOT EXISTS thathvamasi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE thathvamasi_db;

CREATE TABLE IF NOT EXISTS bookings (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    full_name        VARCHAR(100)  NOT NULL,
    mobile           VARCHAR(20)   NOT NULL,
    email            VARCHAR(100)  NOT NULL,
    event_type       VARCHAR(50)   NOT NULL,
    event_date       DATE          NOT NULL,
    start_time       TIME          NOT NULL,
    end_time         TIME          NOT NULL,
    venue_name       VARCHAR(150)  NOT NULL,
    city             VARCHAR(100)  NOT NULL,
    full_address     TEXT          NOT NULL,
    package          VARCHAR(50)   NOT NULL,
    special_requests TEXT,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contacts (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100) NOT NULL,
    mobile     VARCHAR(20),
    subject    VARCHAR(200),
    message    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS testimonials (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    location   VARCHAR(100),
    rating     INT NOT NULL DEFAULT 5,
    message    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
