CREATE DATABASE email_validation;

USE email_validation;

CREATE TABLE email_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    validations JSON,
    score FLOAT,
    status VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Select * from email_results;

ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'cgi@2025';

FLUSH PRIVILEGES;



