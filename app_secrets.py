
from dynaconf import Dynaconf, Validator
DEFAULT_CONFIG = {
    "LOCAL_DB": True,
    "LOGINS": {
        "admin": "a",
        "student": "s"
    }
}
SETTINGS = Dynaconf(
    settings_files=['.streamlit/secrets.toml'], environments=True,
    validators=[
        Validator("LOCAL_DB",must_exist=False,is_type_of=bool)
    ])
SETTINGS.update(DEFAULT_CONFIG)

print(f"Starting Settings: {SETTINGS.as_dict()}")