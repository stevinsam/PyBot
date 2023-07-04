# Import necessary modules and libraries
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from timedate import get_time_and_date
from weather import get_weather

# Create a Flask app instance
app = Flask(__name__)

# Create a ChatBot instance with specified configurations and logic adapters
chatbot = ChatBot(name = 'PyBot', response_selection_method = get_random_response, storage_adapter = "chatterbot.storage.SQLStorageAdapter", read_only = True, 
        logic_adapters = 
        [{
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.8
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation",
        },
        {
            "import_path": "chatterbot.logic.UnitConversion",
        }])

# Create a ChatterBotCorpusTrainer instance and train the chatbot with specified training data
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("trainingData")

# Define a route to the home page
@app.route("/")
def home():
    return render_template("index.html")

# Define a route to handle user input and return bot response
@app.route("/get")
def get_bot_response():
    # Get user input from HTTP GET request
    userText = request.args.get('msg')
    # Check if user input contains the string 'weather' or 'forecast'
    if "weather" in userText.lower() or "forecast" in userText.lower():
        # Return relevant weather information
        return get_weather(userText)
    # Check if user input contains the string 'time' or 'date'
    elif "time" in userText.lower() or "date" in userText.lower():
        # Return relevant time and date information
        return get_time_and_date(userText)
    else:
        # Get bot response to user input
        bot_response = str(chatbot.get_response(userText))
        # Return bot response
        return bot_response

# Run the app if this is the main script being executed
if __name__ == '__main__':
    app.run(debug=True)
