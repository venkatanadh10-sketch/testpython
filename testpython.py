import os
import re

# Regex patterns for common secrets
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws_secret_access_key\s*=\s*[\"'][0-9a-zA-Z\/+]{40}[\"']",
    "Private Key": r"-----BEGIN PRIVATE KEY-----",
    "Generic API Key": r"(?i)(api|token|key|secret|password)[\"'\s:=]+[\"']?[A-Za-z0-9_\-]{8,}[\"']?",
}

def scan_for_secrets(directory):
    print(f"🔍 Scanning directory: {directory}")
    findings = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.js', '.env', '.yaml', '.yml', '.json', '.txt')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    for name, pattern in SECRET_PATTERNS.items():
                        matches = re.findall(pattern, content)
                        if matches:
                            findings.append((file_path, name, matches))

    if not findings:
        print("✅ No secrets found!")
    else:
        print("⚠️ Possible secrets detected:")
        for file, name, matches in findings:
            print(f"\n[file] {file}\n  → {name}: {len(matches)} match(es)")
    return findings


if __name__ == "__main__":
    target_dir = input("Enter the directory path to scan: ").strip()
    scan_for_secrets(target_dir)
