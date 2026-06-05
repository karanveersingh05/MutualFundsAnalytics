import os

for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith(('.py', '.md', '.ipynb')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if '-' in content:
                content = content.replace('-', '-')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
