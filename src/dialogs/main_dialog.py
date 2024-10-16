from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory
from botbuilder.schema import ChannelAccount
from data.menu_db import MenuDatabase

class MainDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(MainDialog, self).__init__(dialog_id or MainDialog.__name__)

        self.menu_db = MenuDatabase()

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.intro_step,
                    self.menu_step,
                    self.order_step,
                    self.confirm_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not step_context.context.activity.from_property.name:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Welcome to our drive-through! What's your name?")),
            )
        else:
            return await step_context.next(step_context.context.activity.from_property.name)

    async def menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["name"] = step_context.result
        
        menu_items = self.menu_db.get_all_items()
        menu = [item['name'] for item in menu_items]
        
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(f"Hello {step_context.values['name']}! What would you like to order?"),
                choices=menu,
            ),
        )

    async def order_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["order"] = step_context.result.value
        item = self.menu_db.get_item_by_name(step_context.values["order"])
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(f"You've ordered a {item['name']} for ${item['price']}. Is this correct?")),
        )

    async def confirm_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            item = self.menu_db.get_item_by_name(step_context.values["order"])
            await step_context.context.send_activity(
                MessageFactory.text(f"Great! Your order of {item['name']} for ${item['price']} will be ready soon. Please pull up to the window.")
            )
        else:
            await step_context.context.send_activity(
                MessageFactory.text("I'm sorry for the confusion. Let's start over.")
            )
        return await step_context.end_dialog()

