# ui_pdf.py - Bridge connecting Reports UI & Print Logic (< 10 Lines)

from mg_reports_ui import REPORTS_UI_MARKUP
from mg_reports_logic import REPORTS_LOGIC_SCRIPT

PDF_ENGINE_MODULE = REPORTS_UI_MARKUP + REPORTS_LOGIC_SCRIPT
