import os
from typing import get_type_hints, Union

from dotenv import load_dotenv


class AppConfigError(Exception):
    pass


class AppConfig:
    PORT: int = 50051
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    WEAVIATE_URL: str = "http://localhost:8080"
    GOOGLE_APPLICATION_CREDENTIALS: str = os.path.join(os.getcwd(), "..", ".credentials/credentials.json")
    GOOGLE_APPLICATION_TOKEN: str = os.path.join(os.getcwd(), "..", ".credentials/token.json")
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str

    def __init__(self, env):
        load_dotenv()

        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            var_type = get_type_hints(AppConfig)[field]
            try:
                if var_type == bool:
                    value = self._parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                err_msg = 'Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                )

                raise AppConfigError(err_msg)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def _parse_bool(val: Union[str, bool]) -> bool:
        return val if type(val) == bool else val.lower() in ['true', 'yes', '1']
