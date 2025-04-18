# NutriTrack - Personalized Nutrition Tracking App

NutriTrack is a comprehensive web application built with Django that helps users track their nutrition, create personalized diet plans, and get AI-powered nutrition advice.

## Features

- User authentication and profile management
- Personalized diet plans
- Calorie calculator
- Meal suggestions
- Weight tracking
- AI-powered nutrition coach
- Responsive design with light/dark themes

## Setting Up OpenAI API Integration

NutriTrack uses OpenAI's GPT-3.5 API for generating personalized diet plans and providing nutrition advice. To use these features, you need to set up your OpenAI API key:

1. Sign up for an OpenAI account at [OpenAI's website](https://openai.com/)
2. Navigate to the [API Keys page](https://platform.openai.com/api-keys)
3. Create a new API key
4. Copy the API key

### Adding Your API Key to NutriTrack

Open the `nutritrack/settings.py` file and replace the placeholder API key with your actual API key:

```python
# OpenAI API settings
OPENAI_API_KEY = 'your-actual-api-key-here'  # Replace with your actual API key
```

**Important:** Never commit your API key to version control. Consider using environment variables for production environments.

## Installation

1. Clone the repository
   ```
   git clone https://github.com/sanatanisher01/Nutrition-Tracker.git
   cd Nutrition-Tracker
   ```
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1
   OPENAI_API_KEY=your_openai_api_key
   ```
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Usage

1. Access the application at `http://127.0.0.1:8000/`
2. Register a new account or log in
3. Complete your profile and dietary preferences
4. Use the dashboard to track your nutrition and generate diet plans
5. Ask NutriBot for nutrition advice

## AI Features

### AI Diet Plan Generation

The AI diet plan generator creates personalized 7-day meal plans based on your:
- Age, gender, height, and weight
- Activity level
- Weight goals
- Dietary preferences
- Daily calorie target

### NutriBot AI Coach

NutriBot can answer questions about:
- Nutrition advice
- Weight loss/gain strategies
- Dietary restrictions
- Meal suggestions
- Calorie information
- And more!

## Deployment

The application is deployed on Render. To deploy your own instance:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Set the start command: `gunicorn nutritrack.wsgi`
5. Add the required environment variables:
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: Set to 'False' for production
   - `ALLOWED_HOSTS`: Your domain name (e.g., 'your-app.onrender.com')
   - `DATABASE_URL`: This will be automatically set by Render if you add a PostgreSQL database
   - `OPENAI_API_KEY`: Your OpenAI API key

## License

This project is licensed under the MIT License - see the LICENSE file for details.
