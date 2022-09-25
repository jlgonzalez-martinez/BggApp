import os

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="BGAPP",
    environments=True,
    settings_files=["settings.yaml", ".secrets.yaml"],
)

BASE_DIR = os.path.dirname(__file__)
DATA_RESOURCES = os.path.join(BASE_DIR, "_resources")
TEST_RESOURCES = os.path.join(BASE_DIR, "tests", "_resources")
