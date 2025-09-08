from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import render
from django.views import View

import logging

logger = logging.getLogger(__name__)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User
from openai import OpenAI

from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserProfileForm

from django.contrib.auth import get_user_model

client = OpenAI()


# CBV for Index View
class HomeView(View):
    template_name = "core/home.html"

    def get(self, request, conversation_id=None):
        context = {}
        return render(request, self.template_name, context)


class HomeTrantorView(View):
    template_name = "core/home_trantor.html"

    def get(self, request, conversation_id=None):
        # select the latest 3 elements from ExerciseDef

        context = {}
        context["exercise_defs"] = []
        context["tutorials"] = []
        context["quizsets"] = []

        return render(request, self.template_name, context)


# CBV for Index View
class ContactView(View):
    template_name = "core/contact.html"

    def get(self, request, conversation_id=None):
        context = {}
        return render(request, self.template_name, context)


# ================


class UserProfileView2(LoginRequiredMixin, DetailView):
    model = User
    template_name = "core/profile.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.request.user.username)


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "core/profile_edit.html"
    success_url = reverse_lazy("core:profile")  # Include the 'core' namespace
    success_message = "Your profile was updated successfully."

    def get_object(self):
        return self.request.user


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "core/profile_delete_confirm.html"
    success_url = reverse_lazy("account_login")

    def get_object(self):
        """
        Return the profile for the currently logged-in custom user.
        """
        return self.request.user


User = get_user_model()


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "core/profile.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        # Return the current logged-in user
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        return context
