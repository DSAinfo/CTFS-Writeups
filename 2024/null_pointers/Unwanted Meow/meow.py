import re

# Path to .shredded file
file_path = "flag.shredded"
with open(file_path, "rb") as file:
    content = file.read()

# Find all the "meow" occurrences in hex (6d 65 6f 77)
pattern = b"meow"  # "meow" in	 bytes

# Delete the occurrences
modified_content = content.replace(pattern, b"")

# Save modified content
with open("flag.shredded", "wb") as file:
    file.write(modified_content)

print("Todas las ocurrencias de 'meow' han sido eliminadas.")
