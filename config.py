from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="BGAPP",
    environments=True,
    settings_files=["settings.yaml", ".secrets.yaml"],
)
