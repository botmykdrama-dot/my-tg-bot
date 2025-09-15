"""
Plugins package for Telegram Bot

This package contains all the plugin modules that handle specific bot commands.
Each plugin should have a register function to add handlers to the application.
"""

__version__ = "1.0.0"
__author__ = "Telegram Bot"

# Import all plugins here for easy access
from .start import register_start_handler

__all__ = [
    'register_start_handler',
]
