import os
from pydantic_settings import BaseSettings

class DecompilerConfig(BaseSettings):
    # API & Agent Token Management
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    # Model Topology Mapping
    frontend_model: str = "gemini-2.5-flash"
    middleend_model: str = "gemini-2.5-flash"
    backend_model: str = "gemini-2.5-flash"
    analyzer_model: str = "gemini-2.5-pro"

    # Runtime Sandbox Hard Constraints
    sandbox_timeout_seconds: int = 5
    max_self_healing_retries: int = 3
    
    # Exporter Output Directories
    output_dir: str = "./output"
    
    class Config:
        env_file = ".env"

# Instantiated single-source-of-truth configuration
config = DecompilerConfig()