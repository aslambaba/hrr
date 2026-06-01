#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
Customized for: Handwritten Digit Recognition Project
- Suppresses TensorFlow oneDNN warnings
- Handles Django management tasks
"""
import os
import sys

def main():
    """Run administrative tasks."""
    
    # 1. SUPPRESS TENSORFLOW ONEDNN WARNINGS
    # This must be set BEFORE importing tensorflow anywhere in the project
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    # 2. SET DJANGO SETTINGS
    # Based on your project structure: handWrittenDigitRecognition
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'handWrittenDigitRecognition.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command (like runserver)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()