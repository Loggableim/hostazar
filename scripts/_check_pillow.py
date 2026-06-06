#!/usr/bin/env python3
try:
    from PIL import Image
    print("Pillow OK")
except ImportError:
    print("NO_PILLOW")
