from django.conf import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Import the OpenAI client
from openai import OpenAI

# Configure OpenAI client
def get_openai_client():
    # Get the API key from settings
    api_key = settings.OPENAI_API_KEY

    # Log the first few characters of the API key for debugging
    if api_key:
        logger.debug(f"API key starts with: {api_key[:10]}...")
    else:
        logger.error("No API key found in settings")
        raise ValueError("OpenAI API key is missing")

    try:
        # Create a client with the API key
        logger.debug("Using new OpenAI client")
        return OpenAI(api_key=api_key)
    except Exception as e:
        logger.error(f"Error with new OpenAI client: {str(e)}")
        raise

def get_chatbot_response(user_message):
    """Get a response from the AI chatbot based on user message"""
    try:
        # Get the OpenAI client
        client = get_openai_client()

        # Log the request
        logger.debug(f"Sending request to OpenAI for chatbot response: {user_message[:50]}...")

        # Create the completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": "You are NutriBot, a nutrition coach. Provide helpful, accurate nutrition advice. Keep responses concise and practical."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        # Return the response
        return completion.choices[0].message.content

    except Exception as e:
        logger.error(f"Failed to get chatbot response: {str(e)}")
        # Provide a helpful response for common diet questions as a fallback
        user_message_lower = user_message.lower()

        if 'diet' in user_message_lower or 'meal plan' in user_message_lower:
            return "A balanced diet should include a variety of fruits, vegetables, lean proteins, whole grains, and healthy fats. For personalized diet advice, consider your specific goals, activity level, and any dietary restrictions you may have."

        elif 'calorie' in user_message_lower:
            return "Calorie needs vary based on age, gender, weight, height, and activity level. For weight maintenance, women typically need 1,600-2,400 calories per day, while men need 2,000-3,000 calories. For weight loss, create a deficit of 500-1000 calories per day through diet and exercise."

        elif 'protein' in user_message_lower:
            return "Good protein sources include lean meats, poultry, fish, eggs, dairy, legumes, tofu, and tempeh. The recommended daily intake is about 0.8g per kg of body weight for the average adult, or higher (1.2-2.0g/kg) for those who are very active or looking to build muscle."

        elif 'vegetarian' in user_message_lower or 'vegan' in user_message_lower:
            return "For a balanced vegetarian or vegan diet, focus on plant proteins like legumes, tofu, tempeh, and seitan. Include a variety of fruits, vegetables, whole grains, nuts, and seeds. Consider supplementing with vitamin B12, vitamin D, omega-3s, iron, and zinc, especially for vegans."

        elif 'weight loss' in user_message_lower:
            return "For sustainable weight loss, create a calorie deficit through a combination of diet and exercise. Focus on nutrient-dense foods, adequate protein (to preserve muscle), plenty of fiber, and staying hydrated. Aim for 1-2 pounds of weight loss per week."

        else:
            return "I'm currently having trouble connecting to my knowledge base. For nutrition advice, focus on whole foods, adequate protein, fruits and vegetables, whole grains, and healthy fats. Stay hydrated and consider your individual needs based on your goals and activity level."

def generate_diet_plan(user_profile, diet_preferences):
    """Generate a personalized diet plan based on user profile and preferences"""
    try:
        # Get the OpenAI client
        client = get_openai_client()

        # Log the request
        logger.debug(f"Sending request to OpenAI for diet plan generation")

        # Create a detailed prompt based on user data
        prompt = f"""
        Generate a 7-day meal plan for a {user_profile.age} year old {user_profile.get_gender_display()},
        height: {user_profile.height}cm, weight: {user_profile.weight}kg,
        activity level: {user_profile.get_activity_level_display()},
        goal: {user_profile.get_goal_display()},
        dietary preferences: {diet_preferences.get_diet_type_display() if diet_preferences else 'No specific preferences'}.
        Daily calorie target: {user_profile.daily_calories} calories.

        Format the response as a structured meal plan with:
        - Breakfast (approx. 25% of daily calories)
        - Lunch (approx. 30% of daily calories)
        - Dinner (approx. 30% of daily calories)
        - Snacks (approx. 15% of daily calories)

        For each meal, include:
        1. Name of the dish
        2. Brief list of ingredients
        3. Approximate calories
        4. Macronutrients (protein, carbs, fat)

        Organize by day (Monday through Sunday).
        """

        # Create the completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": "You are a professional nutritionist specializing in personalized meal plans."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
        )

        # Return the response
        return completion.choices[0].message.content

    except Exception as e:
        error_message = str(e)
        logger.error(f"Failed to generate diet plan: {error_message}")

        # Check for specific error types
        if "high demand" in error_message.lower() or "rate limit" in error_message.lower() or "429" in error_message:
            return """# AI Diet Plan Generation

**The AI service is currently experiencing high demand.**

Please try again in a few moments. Our AI nutritionist is helping many users right now and will be available to create your personalized meal plan shortly.

In the meantime, here are some general nutrition tips:

1. **Focus on whole foods** - Prioritize fruits, vegetables, lean proteins, whole grains, and healthy fats
2. **Stay hydrated** - Aim for 8-10 glasses of water daily
3. **Control portions** - Be mindful of serving sizes
4. **Limit processed foods** - Reduce intake of foods high in added sugars, sodium, and unhealthy fats
5. **Eat regularly** - Aim for 3 balanced meals and 1-2 healthy snacks daily

Your personalized meal plan will be based on your specific profile data and dietary preferences when you try again.

*Click the "Generate AI Plan" button to try again.*
"""
        elif "quota" in error_message.lower() or "insufficient_quota" in error_message:
            return """# AI Diet Plan Generation

**API quota exceeded.**

The OpenAI API quota has been exceeded. Please check your API key and billing details.

To resolve this issue:
1. Verify your OpenAI API key is valid
2. Check your billing status on the OpenAI platform
3. Consider upgrading your plan if you're on a free tier

In the meantime, you can create a manual diet plan by adding meals to your plan directly.

*Contact the administrator if this issue persists.*
"""
        else:
            # Provide a fallback diet plan for other errors
            diet_type = diet_preferences.get_diet_type_display() if diet_preferences else 'Standard'
            daily_calories = user_profile.daily_calories or 2000
            gender = user_profile.get_gender_display()
            age = user_profile.age

            return f"""# 7-Day Meal Plan for {gender}, {age} years old

**Daily Calorie Target:** {daily_calories} calories
**Diet Type:** {diet_type}

## Monday

### Breakfast (approx. {int(daily_calories * 0.25)} calories)
- **Oatmeal with Fruits and Nuts**
  - Ingredients: 1 cup rolled oats, 1 banana, 1 tbsp honey, 10 almonds, 1 cup almond milk
  - Calories: {int(daily_calories * 0.25)}
  - Macros: 15g protein, 60g carbs, 10g fat

### Lunch (approx. {int(daily_calories * 0.3)} calories)
- **Grilled Chicken Salad**
  - Ingredients: 150g grilled chicken breast, mixed greens, cherry tomatoes, cucumber, 1 tbsp olive oil, lemon juice
  - Calories: {int(daily_calories * 0.3)}
  - Macros: 35g protein, 15g carbs, 15g fat

### Dinner (approx. {int(daily_calories * 0.3)} calories)
- **Baked Salmon with Quinoa and Vegetables**
  - Ingredients: 150g salmon fillet, 1 cup cooked quinoa, roasted broccoli and carrots, 1 tbsp olive oil
  - Calories: {int(daily_calories * 0.3)}
  - Macros: 30g protein, 40g carbs, 15g fat

### Snack (approx. {int(daily_calories * 0.15)} calories)
- **Greek Yogurt with Berries**
  - Ingredients: 1 cup Greek yogurt, 1/2 cup mixed berries, 1 tsp honey
  - Calories: {int(daily_calories * 0.15)}
  - Macros: 20g protein, 15g carbs, 5g fat

*Note: This is a sample meal plan generated as a fallback when the AI service is unavailable. Please adjust portions and ingredients based on your specific needs and preferences.*"""
