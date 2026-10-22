import os
import re
import sys

base_dir = r"c:\Users\dell\Desktop\project 2"
terms = [
    'card', 'cards', 'velocity', 'haversine', 'required_speed',
    'travel_speed', 'distance_miles', 'merchant_risk', 'time_delta', 'impossible travel'
]
# Case-insensitive substring match
pattern = re.compile(r'(' + '|'.join(re.escape(t) for t in terms) + r')', re.IGNORECASE)

results = {}

for root, dirs, files in os.walk(base_dir):
    # Only ignore __pycache__, .git, .vscode, and external backup dirs
    if any(ignore in root.lower() for ignore in ['__pycache__', '.git', '.vscode', 'backup']):
        continue
    for f in files:
        if f in ['card_search_matches.txt', 'search_card_terms.py']:
            continue
        filepath = os.path.join(root, f)
        rel = os.path.relpath(filepath, base_dir)
        ext = os.path.splitext(f)[1].lower()

        # Check binary file names
        if ext in ['.pptx', '.pdf', '.jpg', '.png']:
            if pattern.search(f):
                results[rel] = [(0, f"Binary filename match: {f}", [f])]
            continue

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                file_matches = []
                for line_num, line in enumerate(fp, 1):
                    found = pattern.findall(line)
                    if found:
                        file_matches.append((line_num, line.strip()[:140], list(set(found))))
                if file_matches:
                    results[rel] = file_matches
        except Exception as e:
            pass

out_path = os.path.join(base_dir, "card_search_matches.txt")
with open(out_path, "w", encoding="utf-8") as out:
    out.write(f"PROJECT AEGIS - CARD TERMS AUDIT SEARCH REPORT\n")
    out.write(f"=" * 60 + "\n")
    out.write(f"Total matching files: {len(results)}\n\n")

    for path, matches in sorted(results.items()):
        out.write(f"File: {path} (Matches: {len(matches)})\n")
        out.write("-" * 50 + "\n")
        for line_num, line_text, found_terms in matches:
            if line_num == 0:
                out.write(f"  {line_text}\n")
            else:
                out.write(f"  [L{line_num}] [{', '.join(found_terms)}] {line_text}\n")
        out.write("\n")

print(f"Audit completed: {len(results)} files have matching card terms.")
for path in sorted(results.keys()):
    print(f" - {path} ({len(results[path])} matches)")
