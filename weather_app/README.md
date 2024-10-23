# Explanation
This case study was very interesting to work on. I used a simple Tkinter interface this time. For the bounding box, I downloaded a CSV file containing all the cities in the world along with their coordinates (hopefully the data is accurate). I utilized an SQLite3 database to store the API key, city data, and weather information. The main logic of the project can be found in the main_frame.py file. I’m happy with how it turned out, but I’m open to any feedback you may have.

# Install guide

## Local installation

### Virtual environment

Create a virtual environment and active with the following command:

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

### Install dependencies

```bash
python app.py
```

# Improvements
Since the application uses the OpenWeatherMap API, I’ve been considering how to ensure API requests stay within their rate limits. My approach would be to implement a message queue system (e.g., Celery) to manage these tasks, possibly incorporating a retry mechanism with celery.apply_async and a countdown for retries after a few seconds. With the database in place, I can display the cached weather data while waiting for new updates. However, when it comes to handling larger regions efficiently, I don't have a solid solution in mind yet, so I’d be happy to hear your suggestions.