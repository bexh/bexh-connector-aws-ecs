import os
import importlib


def handler():
    module = os.environ.get("MODULE")
    app_name = os.environ.get("APP_NAME")
    command_module = importlib.import_module(module)
    command_module.invoke()


if __name__ == "__main__":
    handler()
