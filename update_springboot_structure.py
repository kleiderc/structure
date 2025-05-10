# Import standard libraries
import os   # For interacting with the filesystem (creating folders, listing files)
import sys  # For handling command-line arguments

# --------------------------------------
# STEP 1: Parse base package from command-line
# --------------------------------------

# Ensure the user passed exactly one argument: the base package
if len(sys.argv) != 2:
    print("❌ Usage: python update_springboot_structure.py com.example.demo")
    sys.exit(1)  # Exit the script with error code 1

# Store the base package name (e.g., "com.example.demo")
base_package = sys.argv[1]

# Convert the package to a file path (e.g., "com/example/demo")
# os.sep ensures platform-independent separator (/ on Linux/Mac, \ on Windows)
base_package_path = base_package.replace(".", os.sep)

# --------------------------------------
# STEP 2: Define the layered structure you want to enforce
# --------------------------------------

# --------------------------------------
# Step 2: Define folders to create
# --------------------------------------
# List of standard packages to check/create inside the base package
packages = [
    "controller",      # REST Controllers (API endpoints)
    "service",         # Service interfaces (business logic contracts)
    "aspect",    	   # AOP allows you to separate cross-cutting concerns (like logging, security, transactions, auditing) from the core business logic
    "repository",      # JPA or JDBC Repositories
    "model",           # Domain/entity classes
    "dto",             # Data Transfer Objects (used in APIs)
    "mapper",          # Classes to map DTOs to models and vice versa
    "config",          # Contains configuration classes, where you configure application settings, or AppConfig
    "exception",       # Custom exceptions and exception handlers
    "util",            # Helper or utility classes
    "factory",         # A Job Factory is a design pattern used to dynamically generate Spring Batch Jobs
    "job"			   # This layer structure revolves around designing and organizing how batch jobs are created, configured, and executed.
]

# Standard Maven Java source folders
src_main_java = os.path.join("src", "main", "java")     # e.g., src/main/java
src_test_java = os.path.join("src", "test", "java")     # e.g., src/test/java
resources_dir = os.path.join("src", "main", "resources")  # Resource folder for configs, templates, static files

# --------------------------------------
# STEP 3: Define helper functions for directory and .gitkeep file handling
# --------------------------------------

def create_directory(path):
    """
    Creates a directory (including parent directories if needed).
    If the directory is empty, adds a .gitkeep file.
    If it already exists, checks whether .gitkeep should be added or removed.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Created: {path}")
    else:
        print(f"✔️ Already exists: {path}")

    # Add or remove .gitkeep depending on whether directory is empty
    handle_gitkeep(path)

def handle_gitkeep(directory):
    """
    Adds a .gitkeep file if the directory is empty (or only contains .gitkeep).
    Removes it if there are real files in the directory.
    """
    gitkeep = os.path.join(directory, ".gitkeep")  # Full path to .gitkeep file

    # List all files except .gitkeep
    files = [f for f in os.listdir(directory) if f != ".gitkeep"]

    if not files:
        # No other files → ensure .gitkeep is there
        if not os.path.exists(gitkeep):
            with open(gitkeep, "w") as f:
                pass  # Just create an empty file
            print(f"🕶️  .gitkeep added to: {directory}")
    else:
        # Directory contains other files → remove .gitkeep if it exists
        if os.path.exists(gitkeep):
            os.remove(gitkeep)
            print(f"🗑️  .gitkeep removed from: {directory} (directory has files)")

# --------------------------------------
# STEP 4: Ensure the base package already exists in the project
# --------------------------------------

# Full path to the base package in main/java (e.g., src/main/java/com/example/demo)
full_base_main_path = os.path.join(src_main_java, base_package_path)

# If this folder doesn't exist, likely not a valid Spring Boot project
if not os.path.exists(full_base_main_path):
    print(f"❌ ERROR: Base package not found at {full_base_main_path}")
    print("➡️ Please make sure you're in a valid Spring Boot project root.")
    sys.exit(1)

# --------------------------------------
# STEP 5: Create main and test Java directories
# --------------------------------------

for p in packages:
    # Convert dot-notation to path (e.g., service.impl → service/impl)
    rel_path = os.path.join(*p.split('.'))

    # Final full path for main and test Java files
    main_path = os.path.join(src_main_java, base_package_path, rel_path)
    test_path = os.path.join(src_test_java, base_package_path, rel_path)

    # Create the directories and manage .gitkeep
    create_directory(main_path)
    create_directory(test_path)

# --------------------------------------
# STEP 6: Create standard resource folders
# --------------------------------------

# Create folders for static assets and templates
create_directory(os.path.join(resources_dir, "static"))      # For CSS, JS, images
create_directory(os.path.join(resources_dir, "templates"))   # For Thymeleaf/Freemarker templates

# Check if application.properties exists; if not, create a default one
application_properties = os.path.join(resources_dir, "application.properties")
if not os.path.exists(application_properties):
    with open(application_properties, "w") as f:
        f.write("# Spring Boot configuration file\n")
    print(f"📝 Created: {application_properties}")
else:
    print("✔️ application.properties already exists.")

# --------------------------------------
# STEP 7: Done
# --------------------------------------

print("\n🎯 Spring Boot project structure updated with .gitkeep handling.")