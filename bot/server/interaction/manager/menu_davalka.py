from telegram import Update
from telegram.ext import ContextTypes

from bot.server.interaction.menu import MenuController
from bot.server.interaction.profile import ProfileController


class MenuDavalka:
    @staticmethod
    def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return MenuController.show_main_menu(update, context)

    @staticmethod
    def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return ProfileController.profile(update, context)
