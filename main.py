from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from timedate import get_time_and_date
from weather import get_weather


app = Flask(__name__)

chatbot = ChatBot(name = 'PyBot', storage_adapter = "chatterbot.storage.SQLStorageAdapter", read_only = False, 
        logic_adapters = 
        [{
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation",
        },
        {
            "import_path": "chatterbot.logic.UnitConversion",
        }])

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("trainingData")



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if "weather" in userText.lower() or "forecast" in userText.lower():
        return get_weather(userText)
    elif "time" in userText.lower() or "date" in userText.lower():
        return get_time_and_date()
    else:
        bot_response = str(chatbot.get_response(userText))
        return bot_response

if __name__ == '__main__':
    # app.debug = True
    app.run()

owm_api_key = config.OWM_API
