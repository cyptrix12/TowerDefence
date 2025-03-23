import os

assets_path = "assets"
qrc_output_path = "assets.qrc"

file_paths = []
for root, dirs, files in os.walk(assets_path):
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), assets_path)
        rel_path = rel_path.replace("\\", "/")
        file_paths.append(f"assets/{rel_path}")

qrc_lines = ['<RCC>', '    <qresource prefix="/">']
for path in sorted(file_paths):
    qrc_lines.append(f'        <file>{path}</file>')
qrc_lines += ['    </qresource>', '</RCC>']

with open(qrc_output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(qrc_lines))
