"""
Пример использования

from pathlib import Path
from preprocessing.stitch_tiles import stitch_tiles_to_ribbon

tile_dir = Path("tiles_inference/film-012/images")  # где лежат тайлы после предсказания
output_path = Path("stitched/film-012.jpg")         # куда сохранить итоговую ленту

stitched_path = stitch_tiles_to_ribbon(tile_dir, output_path)
print(f"Склеенная лента сохранена в: {stitched_path}")
"""

from pathlib import Path
from PIL import Image

def stitch_tiles_to_ribbon(tile_dir: Path, output_path: Path):
    """
    Склеивает предсказанные тайлы 1140×1152 обратно в одну ленту шириной исходного изображения.

    Args:
        tile_dir (Path): Путь к директории с предсказанными тайлами (например, images/film-012/)
        output_path (Path): Путь для сохранения итоговой ленты

    Returns:
        Path: Путь к сохранённой склеенной ленте

    """
    tile_paths = sorted(tile_dir.glob("*.jpg"), key=lambda p: int(p.stem.split("_x")[-1]))
    if not tile_paths:
        raise FileNotFoundError(f"Не найдено ни одного тайла в {tile_dir}")

    # Открываем все тайлы, предполагая одинаковую высоту
    tiles = [Image.open(p) for p in tile_paths]
    tile_height = tiles[0].height
    total_width = sum(t.width for t in tiles)

    # Создаём холст и вставляем тайлы
    stitched = Image.new("RGB", (total_width, tile_height))
    x_offset = 0
    for tile in tiles:
        stitched.paste(tile, (x_offset, 0))
        x_offset += tile.width

    output_path.parent.mkdir(parents=True, exist_ok=True)
    stitched.save(output_path, format="JPEG", quality=100)
    return output_path

