"""
Organize all key files for lecturer panel presentation
"""

import os
from pathlib import Path

# Create presentation folder structure
presentation_folder = Path("c:/Users/hp/.windsurf/2048/PRESENTATION_FILES")

# Key files to organize
key_files = {
    "CORE_APPLICATION": [
        "accounts/views.py",
        "accounts/models.py",
        "items/views.py", 
        "items/models.py",
        "claims/views.py",
        "claims/models.py",
        "reports/views.py",
        "notifications/services.py"
    ],
    
    "CONFIGURATION": [
        "lostfound/settings.py",
        "requirements.txt",
        ".env",
        "Procfile",
        "render.yaml"
    ],
    
    "TEMPLATES": [
        "templates/accounts/admin_dashboard.html",
        "templates/claims/create_claim.html",
        "templates/items/item_detail.html",
        "templates/reports/finder_page.html"
    ],
    
    "TESTING": [
        "DEMONSTRATION_SCRIPT.py",
        "test_otp_claim.py",
        "final_otp_test.py",
        "test_enhanced_sms.py"
    ],
    
    "DOCUMENTATION": [
        "LECTURER_PRESENTATION_GUIDE.md",
        "README.md"
    ]
}

print("MMU Lost & Found - Presentation Files Organizer")
print("=" * 60)

print("\nKEY FILES FOR LECTURER PRESENTATION:")
print("=" * 60)

for category, files in key_files.items():
    print(f"\n{category}:")
    print("-" * 40)
    for file in files:
        file_path = Path(f"c:/Users/hp/.windsurf/2048/{file}")
        if file_path.exists():
            print(f"  READY: {file}")
        else:
            print(f"  MISSING: {file}")

print("\n" + "=" * 60)
print("OPEN THESE FILES IN VS CODE FOR PRESENTATION:")
print("=" * 60)

# Most important files for demonstration
priority_files = [
    "accounts/views.py",          # Admin dashboard
    "claims/models.py",          # OTP system
    "notifications/services.py", # SMS system
    "items/views.py",           # QR codes
    "lostfound/settings.py",    # Configuration
    "templates/accounts/admin_dashboard.html"
]

print("\nPRIORITY FILES (Open these first):")
print("-" * 40)
for file in priority_files:
    print(f"  {file}")

print("\n" + "=" * 60)
print("PRESENTATION READY!")
print("=" * 60)
