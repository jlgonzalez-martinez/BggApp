import os

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="BGAPP",
    environments=True,
    settings_files=["settings.yaml", ".secrets.yaml"],
)

TEST_RESOURCES = os.path.join(os.path.dirname(__file__), "tests", "_resources")
