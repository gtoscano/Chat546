import os
from openai import OpenAI
from django.conf import settings
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.http import JsonResponse

client = OpenAI()


class ChatPageView(TemplateView):
    """Renders the main page with the floating chat window."""

    template_name = "chats/chat_window.html"


class ChatAPI(View):
    """
    Handles POST requests from the chat form (HTMX).
    Returns a partial HTML snippet with user & AI messages.
    """

    def post(self, request, *args, **kwargs):
        user_message = request.POST.get("message", "").strip()
        if not user_message:
            return JsonResponse({"error": "No message provided."}, status=400)

        try:
            prompt = "You are a helpful assistant."

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "text"},
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.3,
            )
            ai_response = response.choices[0].message.content
        except Exception as e:
            ai_response = f"Error: {str(e)}"

        return render(
            request,
            "chats/chat_response.html",
            {
                "user_message": user_message,
                "ai_response": ai_response,
            },
        )
