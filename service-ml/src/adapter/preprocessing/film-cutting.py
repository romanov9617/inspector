"""
Пример использования:

    from pathlib import Path
    from preprocessing.tile_cutter import save_image_tiles, clear_output_dir

    # Очистить и подготовить выходную директорию
    output_dir = Path("cutting_dataset")
    clear_output_dir(output_dir)

    # Путь к исходной рентгеновской ленте (1152 px по высоте, ширина 31920 px)
    image_path = Path(...)

    # Нарезка изображения на тайлы 1140x1152 и сохранение
    num_tiles = save_image_tiles(image_path, output_dir)

    print(f"Сохранено тайлов: {num_tiles}")
"""


from pathlib import Path
from PIL import Image
import shutil

# === Правильные размеры тайлов ===
TILE_WIDTH = 1140    # ширина одного тайла
TILE_HEIGHT = 1152   # высота одного тайла
STRIDE = TILE_WIDTH  # без overlap

def clear_output_dir(output_dir: Path):
    """Удаляет и пересоздаёт директорию с поддиректорией images/."""
    shutil.rmtree(output_dir, ignore_errors=True)
    (output_dir / "images").mkdir(parents=True, exist_ok=True)

def get_x_positions(img_w: int) -> list:
    """Возвращает список X-координат начала тайлов шириной TILE_WIDTH без перекрытий."""
    return list(range(0, img_w - TILE_WIDTH + 1, STRIDE))

def save_image_tiles(image_path: Path, out_dir: Path):
    """
    Режет длинную рентгеновскую ленту (31920×1152) на тайлы 1140×1152 без overlap.

    Тайлы сохраняются в:
        {out_dir}/images/{stem}/{stem}_x{position}.jpg

    Args:
        image_path (Path): Путь к изображению ленты
        out_dir (Path): Директория, куда сохраняются тайлы

    Returns:
        int: Количество сохранённых тайлов
    """
    image = Image.open(image_path)
    img_w, img_h = image.size
    stem = image_path.stem

    if img_h != TILE_HEIGHT:
        raise ValueError(f"Ожидается высота изображения {TILE_HEIGHT}, но получено {img_h}")

    image_out_dir = out_dir / "images" / stem
    image_out_dir.mkdir(parents=True, exist_ok=True)

    x_positions = get_x_positions(img_w)

    for x in x_positions:
        tile = image.crop((x, 0, x + TILE_WIDTH, TILE_HEIGHT))
        tile_path = image_out_dir / f"{stem}_x{x}.jpg"
        tile.save(tile_path, format="JPEG", quality=100, optimize=True)

    return len(x_positions)