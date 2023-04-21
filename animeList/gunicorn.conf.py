from config import AppConfig

app_config = AppConfig.load()

bind = '0.0.0.0:{}'.format(app_config.port)
accesslog = '-'