#!/usr/bin/env python
"""Test backend import."""
import sys

try:
    from app.main import app
    print("Backend import successful!")
    print(f"FastAPI app: {app}")
    sys.exit(0)
except Exception as e:
    print(f"Backend import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
