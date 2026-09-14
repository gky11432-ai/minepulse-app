# ui_auth.py - Bridge connecting Auth UI & Role Lock Logic (< 10 Lines)

from mg_auth_ui import AUTH_UI_MARKUP
from mg_auth_lock import AUTH_LOCK_SCRIPT

AUTH_MODULE = AUTH_UI_MARKUP + AUTH_LOCK_SCRIPT
