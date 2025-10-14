import argparse
from dotenv import load_dotenv
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

    try:
        settings = Settings()
        print("APP_NAME:", settings.APP_NAME)
        print("ENVIRONMENT:", settings.ENVIRONMENT)
    except Exception as e:
        print("Error loading settings:", e)
