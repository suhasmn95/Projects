import sys

# Check if the script receives a command-line argument
if len(sys.argv) > 1:
    # Print the first argument (excluding the script name)
    print(f"Command-line argument received: {sys.argv[1]}")
else:
    print("No command-line arguments provided.")
