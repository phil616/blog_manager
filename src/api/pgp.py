from fastapi import APIRouter
from pydantic import BaseModel
from gnupg import GPG
from typing import Optional, Union

gpg_client = GPG()

pgp_router = APIRouter()


class PGPData(BaseModel):
    data: Union[str, bytes]
    passphrase: str


@pgp_router.post("/symmetric_encrypt")
async def encrypt(data: PGPData):
    text = gpg_client.encrypt(data=data.data, recipients="None", passphrase=data.passphrase, symmetric=True)
    return str(text)


@pgp_router.post("/symmetric_decrypt")
async def decrypt(data: PGPData):
    text = gpg_client.decrypt(message=data.data, passphrase=data.passphrase)
    return str(text)
