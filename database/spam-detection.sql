CREATE TABLE spam_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_text TEXT NOT NULL,
    naive_bayes_pred TINYINT,
    xgboost_pred TINYINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
