from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="APP",
    load_dotenv=True,
)