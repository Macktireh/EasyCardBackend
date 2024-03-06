import os


def getEnvVar(varName: str, default: str | None = None, required: bool = True) -> str | None:
    value = os.environ.get(varName, default)
    if required and not value:
        raise Exception(f"Environment variable {varName} is required")
    return value
