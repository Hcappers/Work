from pathlib import Path

# Correct file path with raw string to handle spaces and backslashes
input_file = r"F:\List of files.txt"

# Extensions to look for (case-insensitive)
target_exts = {".txt", ".pdf", ".doc", ".docx"}

# Output file name (will be saved in the same folder as the script)
output_file = "matched_docs.txt"

# Optional: Check if input file exists before proceeding
if not Path(input_file).exists():
    raise FileNotFoundError(f"Input file does not exist: {input_file}")

# Process the input file
with open(output_file, "w", encoding="utf-8") as out:
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            path = line.strip()
            if not path:
                continue
            suffix = Path(path).suffix.lower()
            if not suffix and '.' in Path(path).name:
                suffix = '.' + Path(path).name.split('.')[-1].lower()
            if suffix in target_exts:
                out.write(path + "\n")

print(f"Matching file paths written to: {output_file}")