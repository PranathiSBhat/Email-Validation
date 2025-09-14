CREATE DATABASE email_validation;

USE email_validation;

CREATE TABLE email_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    syntax_check TINYINT(1) DEFAULT 0,
    domain_exists TINYINT(1) DEFAULT 0,
    mx_records TINYINT(1) DEFAULT 0,
    mailbox_exists TINYINT(1) DEFAULT 0,
    is_disposable TINYINT(1) DEFAULT 0,
    is_role_based TINYINT(1) DEFAULT 0,
    score FLOAT DEFAULT 0.0,
    status VARCHAR(255) DEFAULT 'Unknown',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Select * from email_results;

ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'root';

FLUSH PRIVILEGES;



