"""
Configuration for Fake News Verification API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyD0Pr97plYcTfWdBE4MI7HvAceM_rWGzDk")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "f14f0a542cd594aba")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

# LLM Configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "tngtech/deepseek-r1t2-chimera:free"

# App Configuration
APP_NAME = "Fake News Verification API"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
