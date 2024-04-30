from pytmx.util_pygame import load_pygame
import sys

def load_tmx(tmx_file):
    try:
        tmx_data = load_pygame(tmx_file)
    except Exception as e:
        print("Error loading TMX file:", e)
        sys.exit()
    return tmx_data