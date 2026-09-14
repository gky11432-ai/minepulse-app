# ui_sync.py - Bridge connecting DB Vault & Cloud Sync Logic (< 10 Lines)

from mg_vault_db import VAULT_DB_MODULE
from mg_vault_sync import VAULT_SYNC_MODULE

SYNC_SCRIPT = VAULT_DB_MODULE + VAULT_SYNC_MODULE
