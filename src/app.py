from botbuilder.core import BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity, ActivityTypes
from flask import Flask, request, Response
import asyncio

app = Flask(__name__)

# Replace these with your own app ID and app password
APP_ID = "YOUR_APP_ID"
APP_PASSWORD = "YOUR_APP_PASSWORD"

# Create adapter
adapter = BotFrameworkAdapter(APP_ID, APP_PASSWORD)

# Define main bot logic
async def on_turn(turn_context: TurnContext):
    if turn_context.activity.type == ActivityTypes.message:
        text = turn_context.activity.text.lower()
        
        if "hello" in text or "hi" in text:
            await turn_context.send_activity("Welcome to our drive-through! How can I help you today?")
        elif "menu" in text:
            await turn_context.send_activity("Our menu includes burgers, fries, and drinks. What would you like to order?")
        elif "order" in text:
            await turn_context.send_activity("Great! Can you please specify what items you'd like to order?")
        else:
            await turn_context.send_activity("I'm sorry, I didn't understand that. Can you please rephrase or ask for the menu?")

# Set up routes
@app.route("/api/messages", methods=["POST"])
def messages():
    if request.headers.get("Content-Type") == "application/json":
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    
    async def call_on_turn(turn_context):
        await on_turn(turn_context)

    task = asyncio.ensure_future(adapter.process_activity(activity, "", call_on_turn))
    asyncio.get_event_loop().run_until_complete(task)
    
    return Response(status=201)

if __name__ == "__main__":
    app.run(debug=True)
