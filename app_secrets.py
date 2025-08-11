
from dynaconf import Dynaconf, Validator

SETTINGS = Dynaconf(
    settings_files=['.streamlit/config.toml','.streamlit/secrets.toml'], environments=True,envvar_prefix="APP",
    validators=[
        Validator("LOCAL_DB",is_type_of=bool)
    ])

SETTINGS.validators.validate()
print(f"Starting Settings: {SETTINGS.as_dict()}")