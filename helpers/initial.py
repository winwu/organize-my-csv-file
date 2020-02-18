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
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'boxplot')):
            os.makedirs(os.path.join(basepath, 'dist', 'boxplot'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'line_chart')):
            os.makedirs(os.path.join(basepath, 'dist', 'line_chart'), mode = 0o777, exist_ok = True)
    
    finally:
        os.umask(original_umask)

def create_image_folders():
    try:
        original_umask = os.umask(0)
        if not os.path.exists(os.path.join(basepath, 'dist', 'images')):
            os.makedirs(os.path.join(basepath, 'dist', 'images'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'images', 'avg_123')):
            os.makedirs(os.path.join(basepath, 'dist', 'images', 'avg_123'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'images', 'avg_123', 'attention')):
            os.makedirs(os.path.join(basepath, 'dist', 'images', 'avg_123', 'attention'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'images', 'avg_123', 'meditation')):
            os.makedirs(os.path.join(basepath, 'dist', 'images', 'avg_123', 'meditation'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'images', 'avg_23')):
            os.makedirs(os.path.join(basepath, 'dist', 'images', 'avg_23'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'images', 'avg_23', 'attention')):
            os.makedirs(os.path.join(basepath, 'dist', 'images', 'avg_23', 'attention'), mode = 0o777, exist_ok = True)
        
        if not os.path.exists(os.path.join(basepath, 'dist', 'images', 'avg_23', 'meditation')):
            os.makedirs(os.path.join(basepath, 'dist', 'images', 'avg_23', 'meditation'), mode = 0o777, exist_ok = True)
        
    finally:
        os.umask(original_umask)
