from datetime import datetime
from uuid import uuid4
from typing import Literal


def gen_random_string(length: int = 16) -> str:
    return str(uuid4().hex)[:length]


def get_current_time(t: Literal["iso", "Blog"] = "Blog"):
    if t == "iso":
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    elif t == "Blog":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
    else:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def iso_to_datetime(iso_str: str) -> datetime:
    return datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%fZ")


def blogtime_to_datetime(blogt_str: str) -> datetime:
    return datetime.strptime(blogt_str, "%Y-%m-%d %H:%M:%S +0800")
