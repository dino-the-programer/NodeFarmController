from pydantic_settings import BaseSettings

class Config(BaseSettings):
    app_name: str = "NodeFarmController"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "data.db"

    @property
    def db_url(self):
        return f"sqlite:///./{self.db_name}"


config = Config()