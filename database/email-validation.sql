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

DELETE from email_results;

CREATE TABLE spam_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_text TEXT NOT NULL,
    naive_bayes_pred TINYINT,
    xgboost_pred TINYINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * from spam_results;
Delete from spam_results;

CREATE TABLE user_sign (
	name TEXT(30) NOT NULL,
    email varchar(255) NOT NULL,
    password varchar(50) NOT NULL
);

SELECT * from user_sign;

ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'cgi@2025';

FLUSH PRIVILEGES;

