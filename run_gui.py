#!/usr/bin/env python3
"""
Launcher for the integrated YouTube Gaza Data Collector GUI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the GUI
from gui import main

if __name__ == "__main__":
    print("=" * 60)
    print("YouTube Gaza Data Collector - Integrated GUI")
    print("=" * 60)
    print("\nLaunching GUI application...")
    print("The GUI will handle the complete pipeline:")
    print("  1. Configuration input")
    print("  2. Data collection")
    print("  3. PySpark analysis")
    print("  4. Visualization")
    print("  5. Results gallery")
    print("\n" + "=" * 60 + "\n")
    
    main()
