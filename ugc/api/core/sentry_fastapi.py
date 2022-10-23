import os

from sentry_sdk import init
from sentry_sdk.integrations.fastapi import FastApiIntegration


def sentry_init():
    if "SENTRY_DSN" in os.environ.keys():
        init(
            integrations=[FastApiIntegration()],
            traces_sample_rate=os.environ.get("SENTRY_RATE", 0.5))
