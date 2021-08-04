from pathlib import Path

ROOT_PATH = Path().absolute()
while ROOT_PATH.name != "synthesis_proj":
    ROOT_PATH = ROOT_PATH.parent
