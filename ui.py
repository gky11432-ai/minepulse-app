# ui.py - Master UI Assembler with Modular Parts
from ui_part1 import PART1
from ui_offline import OFFLINE_SCRIPT
from ui_part2 import PART2
from ui_part3 import PART3

# Sabhi chhote parts ko seamlessly merge karta hai
HTML = PART1 + PART3 + OFFLINE_SCRIPT + PART2
