# Spam Detection Dashboard

A comprehensive web dashboard for spam detection using XGBoost machine learning model with real-time predictions and performance metrics visualization.

## Features

### 🎯 Real-time Spam Detection
- **Text Classification**: Enter any text to get instant spam/ham classification
- **Confidence Scores**: See confidence percentages for both spam and ham predictions
- **Visual Feedback**: Color-coded results with progress bars

### 📊 Performance Metrics
- **Model Accuracy**: Overall accuracy of the XGBoost model
- **Precision & Recall**: Detailed performance metrics
- **F1 Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Visual representation of true/false positives and negatives

### 📈 Dashboard Features
- **Modern UI**: Responsive design with gradient backgrounds and smooth animations
- **Real-time Updates**: Auto-refreshing metrics and recent results
- **Interactive Charts**: Visual representation of model performance
- **Recent History**: View all recent classifications with timestamps

## API Endpoints

### 1. Predict Spam
```http
POST /api/spam/predict
Content-Type: application/json

{
    "text": "Your text to classify"
}
```

**Response:**
```json
{
    "text": "Your text to classify",
    "prediction": "Spam",
    "confidence": {
        "ham": 15.23,
        "spam": 84.77
    },
    "is_spam": true
}
```

### 2. Get Model Metrics
```http
GET /api/spam/metrics
```

**Response:**
```json
{
    "confusion_matrix": [[45, 5], [3, 47]],
    "accuracy": 0.92,
    "precision": 0.9038,
    "recall": 0.94,
    "f1_score": 0.9216,
    "total_samples": 100,
    "true_negatives": 45,
    "false_positives": 5,
    "false_negatives": 3,
    "true_positives": 47
}
```

### 3. Get Recent Results
```http
GET /api/spam/results
```

**Response:**
```json
[
    {
        "id": 1,
        "email_text": "Sample text",
        "xgboost_pred": 1,
        "created_at": "2024-01-15 10:30:00"
    }
]
```

## Setup Instructions

### 1. Prerequisites
- Python 3.7+
- MySQL database
- XGBoost model files (`xgboost_model.pkl` and `vectorizer.pkl`)

### 2. Database Setup
Make sure your MySQL database has the `spam_results` table:

```sql
CREATE TABLE spam_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_text TEXT NOT NULL,
    naive_bayes_pred TINYINT,
    xgboost_pred TINYINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Install Dependencies
```bash
pip install flask mysql-connector-python scikit-learn xgboost pandas numpy
```

### 4. Populate Sample Data (Optional)
```bash
python populate_spam_data.py
```

### 5. Run the Application
```bash
python run_app.py
```

### 6. Access the Dashboard
Open your browser and navigate to:
- **Dashboard**: http://127.0.0.1:5000/spam-dashboard
- **API Documentation**: Available at the endpoints listed above

## Testing

### Run Test Suite
```bash
python test_spam_dashboard.py
```

This will test:
- Spam prediction API with sample texts
- Metrics API functionality
- Results API data retrieval

### Manual Testing
1. Open the dashboard in your browser
2. Enter sample texts in the classification form
3. Verify predictions and confidence scores
4. Check that metrics are displayed correctly
5. Verify recent results are updated

## Sample Test Texts

### Spam Examples
- "Congratulations! You've won $1000! Click here to claim your prize now!"
- "URGENT: Your account will be suspended unless you verify your information immediately!"
- "FREE MONEY! No strings attached! Get rich quick with this amazing opportunity!"

### Ham Examples
- "Hi, how are you doing today? I hope you're having a great week."
- "Thanks for your email. I'll get back to you by tomorrow."
- "The meeting has been scheduled for 3 PM tomorrow in the conference room."

## Technical Details

### Model Architecture
- **Algorithm**: XGBoost Classifier
- **Vectorization**: TF-IDF with 1000 features
- **Preprocessing**: English stop words removal
- **Labels**: 0 = Ham, 1 = Spam

### Performance Features
- **Real-time Prediction**: Sub-second response times
- **Confidence Scoring**: Probability-based confidence levels
- **Database Storage**: All predictions stored for analysis
- **Auto-refresh**: Metrics update every 30 seconds

### UI/UX Features
- **Responsive Design**: Works on desktop and mobile
- **Modern Styling**: Gradient backgrounds and smooth animations
- **Interactive Elements**: Hover effects and loading states
- **Error Handling**: User-friendly error messages

## Troubleshooting

### Common Issues

1. **Model Not Loading**
   - Check that `xgboost_model.pkl` and `vectorizer.pkl` exist in `ml_model/` folder
   - Verify file paths in `app.py`

2. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in `db_connection()` function
   - Verify `spam_results` table exists

3. **No Metrics Displayed**
   - Run `populate_spam_data.py` to add sample data
   - Check that predictions have been made (stored in database)

4. **Prediction Errors**
   - Ensure text input is not empty
   - Check that model files are properly loaded
   - Verify TF-IDF vectorizer compatibility

### Debug Mode
Enable Flask debug mode by setting `debug=True` in `app.py` for detailed error messages.

## File Structure

```
Email-Validation/
├── app.py                          # Main Flask application
├── templates/
│   └── spam_dashboard.html         # Dashboard HTML template
├── ml_model/
│   ├── xgboost_model.pkl          # Trained XGBoost model
│   └── vectorizer.pkl             # TF-IDF vectorizer
├── database/
│   └── spam-detection.sql         # Database schema
├── test_spam_dashboard.py         # Test suite
├── populate_spam_data.py          # Sample data generator
└── SPAM_DASHBOARD_README.md       # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Email Validation system. Please refer to the main project license for usage terms.

