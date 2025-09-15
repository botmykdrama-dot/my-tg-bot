"""
Helpers package for Telegram Bot

This package contains helper modules that provide utility functions 
and additional command handlers for the bot.
"""

__version__ = "1.0.0"
__author__ = "Telegram Bot"

# Import all helpers here for easy access
from .help import register_help_handler

__all__ = [
    'register_help_handler',
]
