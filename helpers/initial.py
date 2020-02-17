import os
from pathlib import Path

basepath = Path(__file__).parent.parent

def create_folders():
    # create folder if not exists
    try:
        original_umask = os.umask(0)
        if not os.path.exists(os.path.join(basepath, 'dist', 'by_tester')):
            os.makedirs(os.path.join(basepath, 'dist', 'by_tester'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'by_alphabet')):
            os.makedirs(os.path.join(basepath, 'dist', 'by_alphabet'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'by_alphabet_describe')):
            os.makedirs(os.path.join(basepath, 'dist', 'by_alphabet_describe'), mode = 0o777, exist_ok = True)
    finally:
        os.umask(original_umask)