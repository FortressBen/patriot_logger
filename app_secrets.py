
from dynaconf import Dynaconf, Validator
DEFAULT_CONFIG = {
    "LOCAL_DB": True,
    "LOGINS": {
        "admin": "a",
        "student": "s"
    }
}
SETTINGS = Dynaconf(
    settings_files=['.streamlit/secrets.toml'], environments=True,envvar_prefix="APP",
    validators=[
        Validator("LOCAL_DB",is_type_of=bool)
    ])
SETTINGS.update(DEFAULT_CONFIG)
SETTINGS.validators.validate()
print(f"Starting Settings: {SETTINGS.as_dict()}")