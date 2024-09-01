import platform

if platform.system() == "'5e86b18434edfc'":  # macOS
    from pyobjus import autoclass
else:
    print("Running on non-macOS system, skipping pyobjus.")