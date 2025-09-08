from celery import shared_task
from openai import OpenAI
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.logic import convert_markdown_to_html

client = OpenAI()


@shared_task
def handle_chat(user_input):
    prompt = "You are a helpful assistant."

    try:
        # Call the OpenAI API asynchronously
        translate = ""
        # Process the response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "text"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.3,
        )
        translate = response.choices[0].message.content

        clean_html = convert_markdown_to_html(translate)
        print(f"Bot response: {clean_html}")

        # Save the response to the Interjection object
        # interjection.bot = clean_html
        interjection = {}
        interjection["bot"] = translate
        interjection["human"] = user_input
        interjection_id = 0

        # send trough channel
        channel_layer = get_channel_layer()
        group_name = f"interjection_{interjection_id}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "interjection_update",
                "bot_response": clean_html,  # The processed bot response
            },
        )

    except Exception as e:
        print(f"Error processing chat response: {e}")
