import os
import argparse
from dotenv import load_dotenv
import yaml
from src.settings import Settings


def export_envs(environment: str = "dev") -> None:
    env_file_map = {
        "dev": "config/.env.dev",
        "test": "config/.env.test",
        "prod": "config/.env.prod",
    }
    env_path = env_file_map.get(environment)
    if not env_path:
        raise ValueError(
            f"Invalid environment '{environment}'. Must be one of: dev, test, prod."
        )
    load_dotenv(dotenv_path=env_path, override=True)


def export_secrets(file_path: str = "secrets.yaml") -> None:
    try:
        with open(file_path, "r") as f:
            secrets = yaml.safe_load(f)
        for key, value in secrets.items():
            os.environ[key] = str(value)
    except Exception as e:
        print(f"Error loading secrets: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load environment variables from specified .env file."
    )
    parser.add_argument(
        "--environment",
        type=str,
        default="dev",
        help="The environment to load (dev, test, prod)",
    )
    args = parser.parse_args()

    export_envs(args.environment)
    export_secrets("secrets.yaml")

    try:
        settings = Settings()
        print("APP_NAME:", settings.APP_NAME)
        print("ENVIRONMENT:", settings.ENVIRONMENT)
        print("FAKE_API_KEY:", settings.FAKE_API_KEY)
    except Exception as e:
        print("Error loading settings:", e)
