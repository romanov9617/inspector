import os
from pathlib import Path

download_dir = os.getenv("DOWNLOAD_DIR", "./tmp/")
# Path(download_dir).mkdir(parents=True, exist_ok=True)
# Имя локального файла — берём имя объекта
filename = Path("/".join("inspector/uploads/4/0-250-ls-r1-1-23nv.png".split("/")[1:]))
local_path = os.path.join(download_dir, os.path.dirname(filename))
print(local_path)
os.makedirs(local_path, exist_ok=True)
