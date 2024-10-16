from botbuilder.core import BotFrameworkAdapter, ConversationState, MemoryStorage, TurnContext
from botbuilder.dialogs import DialogExtensions
from botbuilder.schema import Activity
from flask import Flask, request, Response
from dialogs.main_dialog import MainDialog
import asyncio

app = Flask(__name__)

# Replace these with your own app ID and app password
APP_ID = "YOUR_APP_ID"
APP_PASSWORD = "YOUR_APP_PASSWORD"

# Create adapter and conversation state
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
ADAPTER = BotFrameworkAdapter(APP_ID, APP_PASSWORD)

# Create dialog
DIALOG = MainDialog()

# Define main bot logic
async def on_turn(turn_context: TurnContext):
    dialog_context = await DIALOG.create_context(turn_context)
    results = await dialog_context.continue_dialog()
    
    if results.status == DialogTurnStatus.Empty:
        await dialog_context.begin_dialog(DIALOG.id)

    await CONVERSATION_STATE.save_changes(turn_context)

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

    task = asyncio.ensure_future(ADAPTER.process_activity(activity, "", call_on_turn))
    asyncio.get_event_loop().run_until_complete(task)
    
    return Response(status=201)

if __name__ == "__main__":
    app.run(debug=True)

