from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    token: str
    admin_code: str
    channel_id: int

def load_config() -> Config:
    env = Env()
    env.read_env()
    
    return Config(
        token=env.str('BOT_TOKEN', '2027076146:AAF71gnNupo1gGYlBXAcJdQc6XJJLHsIusg'),  # Перенесите токен в .env файл в реальном проекте
        admin_code=env.str('ADMIN_CODE', 'asdjk;laskjnvajllkajsdlkj'),
        channel_id=env.int('CHANNEL_ID', -1001509319502)
    ) 