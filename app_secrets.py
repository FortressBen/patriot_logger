
from dynaconf import Dynaconf, Validator

SETTINGS = Dynaconf(
    settings_files=['.streamlit/config.toml','.streamlit/secrets.toml'], environments=True,envvar_prefix="APP",
    validators=[
        Validator("LOCAL_DB",is_type_of=bool)
    ])

DEFAULT_DB_PATH="mann_xc.duckdb"
SETTINGS.validators.validate()

if "LOCAL_DB" not in SETTINGS.as_dict():
    print(f"Warning: LOCAL_DB not set, assuming True")
    SETTINGS['LOCAL_DB'] = True

if SETTINGS['LOCAL_DB'] == True:
    if not "DB_PATH" in SETTINGS.as_dict().keys():
        print(f"Warning: LOCAL_DB= True, but DB_PATH not set, using {DEFAULT_DB_PATH}")
        db_path = SETTINGS['DB_PATH'] =DEFAULT_DB_PATH

print(f"Starting Settings: {SETTINGS.as_dict()}")