import os
from collections import Counter
import time

def countFiles(path):
    file_counter = Counter()
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                ext = os.path.splitext(entry.name)[1].lower() or "[no extension]"
                file_counter[ext] += 1
            elif entry.is_dir():
                file_counter += countFiles(entry.path)
    except (PermissionError, OSError) as error:
        print(f"Skipping inaccessible folder: {error}")
    return file_counter

def main():
    path = input("Enter the path you want to scan: ").strip()
    while not os.path.isdir(path):
        print("The path you entered is not a valid directory.")
        path = input("Enter the path you want to scan: ").strip()
    
    defaultOutput = f"fileStats_{time.strftime('%Y%m%d')}"
    print(f"Default output file name is: {defaultOutput}")

    while True:
        nameChoice = input("Enter 1 for default name or 2 for custom name: ").strip()
        if nameChoice == "1":
            output = defaultOutput
            break
        elif nameChoice == "2":
            output = input("Enter the output file name (no extension): ").strip()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    while True:
        formatChoice = input("Enter 1 for TXT or 2 for CSV: ").strip()
        if formatChoice == "1":
            outputfile = os.path.join(path, f"{output}.txt")
            fileFormat = "txt"
            break
        elif formatChoice == "2":
            outputfile = os.path.join(path, f"{output}.csv")
            fileFormat = "csv"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    print(f"Scanning {path} (may take a few minutes)...")
    startTime = time.time()

    fileStats = countFiles(path)
    totalFiles = sum(fileStats.values())

    with open(outputfile, "w") as file:
        if fileFormat == "csv":
            file.write("Extension,Count\n")  # No space after comma for cleaner CSV
            for ext, count in sorted(fileStats.items(), key=lambda x: x[1], reverse=True):
                file.write(f"{ext},{count}\n")
        else:
            file.write("Extension\tCount\n")
            for ext, count in sorted(fileStats.items(), key=lambda x: x[1], reverse=True):
                file.write(f"{ext}\t{count}\n")
    
    timeTaken = time.time() - startTime
    print(f"Finished in {timeTaken:.1f} seconds")
    print(f"Total files: {totalFiles}")
    print("Top 10 file types:")
    for ext, count in fileStats.most_common(10):
        print(f"{ext}: {count}")
    print(f"Results saved to: {outputfile}")

if __name__ == "__main__":
    main()