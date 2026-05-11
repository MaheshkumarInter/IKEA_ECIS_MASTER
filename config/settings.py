import os
from config.env_credentials import ENV_CRED


ENV = os.getenv("TEST_ENV", "test")  # default = test

BASE_URLS = ENV_CRED[ENV]