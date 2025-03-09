"""
utils.db.py
---
Author: Enitoxy
Co-authors: [empty]
License: GPL-3.0
Description: A utility that connects to a MongoDB database
"""

import logging
import os
from glob import glob

from pymongo import AsyncMongoClient

MONGODB = os.getenv("MONGODB")

log = logging.getLogger(__name__)

# Place a single X509 certificate at the root of the project, in certs/
cert = glob("./certs/X509-cert*.pem")
client = AsyncMongoClient(
    f"mongodb+srv://{MONGODB}",
    authSource="$external",
    authMechanism="MONGODB-X509",
    retryWrites=True,
    w="majority",
    tls=True,
    tlsCertificateKeyFile=cert[0],
)
log.info("Database client set up")

# From the client, we get a database by its name
db = client["excla2"]

# Then we get a collection, in this case it's named inventory
inventory = db["inventory"]
