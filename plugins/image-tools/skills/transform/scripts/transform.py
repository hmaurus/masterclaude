#!/usr/bin/env python3
"""
Image Transform Tool
Redimensionar, rotacionar, espelhar, recortar e converter imagens com Pillow.
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Erro: Pillow não instalado. Execute setup.sh primeiro.", file=sys.stderr)
    sys.exit(1)

SUPPORTED_INPUT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".tif", ".ico"}
FORMAT_MAP = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP",
              "gif": "GIF", "bmp": "BMP", "tiff": "TIFF", "tif": "TIFF"}


def parse_resize(value):
    parts = value.lower().split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            f"Formato inválido: '{value}'. Use WxH (ex: 800x600)"
        )
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Dimensões devem ser inteiros: '{value}'"
        )


def parse_crop(value):
    parts = value.split(",")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            f"Formato inválido: '{value}'. Use L,T,R,B (ex: 100,50,500,400)"
        )
    try:
        return tuple(int(p.strip()) for p in parts)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Coordenadas devem ser inteiros: '{value}'"
        )


def determine_paths(input_path: Path, args):
    """
    Retorna (output_path, backup_path_or_None).
    - Se --output: salva no destino, sem backup.
    - Se --suffix: salva com sufixo, sem backup.
    - Caso contrário (in-place): renomeia original para _original, salva no nome original.
    - Se --no-backup: in-place sem backup.
    """
    input_ext = input_path.suffix  # ex: '.jpg'
    output_ext = ("." + args.format) if args.format else input_ext

    if args.output:
        out = Path(args.output).expanduser()
        if out.is_dir() or str(args.output).endswith("/"):
            out.mkdir(parents=True, exist_ok=True)
            out_file = out / (input_path.stem + output_ext)
        else:
            out_file = out
        return out_file, None

    if args.suffix:
        out_file = input_path.parent / (input_path.stem + args.suffix + output_ext)
        return out_file, None

    # In-place
    out_file = input_path.parent / (input_path.stem + output_ext)
    if args.no_backup:
        return out_file, None

    # Backup: não duplicar se já termina em _original
    stem = input_path.stem
    if stem.endswith("_original"):
        return out_file, None

    backup_path = input_path.parent / (stem + "_original" + input_ext)
    return out_file, backup_path


def get_fill_color(img: Image.Image):
    """Retorna cor de preenchimento adequada ao modo da imagem."""
    if img.mode in ("RGBA", "LA"):
        return (0, 0, 0, 0)  # transparente
    if img.mode == "RGB":
        return (255, 255, 255)  # branco
    return None  # Pillow decide


def prepare_for_jpeg(img: Image.Image) -> Image.Image:
    """Converte para RGB se necessário para salvar como JPEG."""
    if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        src = img.convert("RGBA") if img.mode == "P" else img
        if src.mode in ("RGBA", "LA"):
            background.paste(src, mask=src.split()[-1])
        else:
            background.paste(src)
        return background
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def apply_transforms(img: Image.Image, args) -> Image.Image:
    """Aplica todas as transformações na ordem: resize → crop → rotate → flip."""

    # --- Resize (apenas uma das opções) ---
    if args.resize:
        w, h = args.resize
        img = img.resize((w, h), Image.LANCZOS)

    elif args.scale is not None:
        factor = args.scale / 100.0
        new_w = max(1, int(img.width * factor))
        new_h = max(1, int(img.height * factor))
        img = img.resize((new_w, new_h), Image.LANCZOS)

    elif args.fit_width is not None:
        ratio = args.fit_width / img.width
        new_h = max(1, int(img.height * ratio))
        img = img.resize((args.fit_width, new_h), Image.LANCZOS)

    elif args.fit_height is not None:
        ratio = args.fit_height / img.height
        new_w = max(1, int(img.width * ratio))
        img = img.resize((new_w, args.fit_height), Image.LANCZOS)

    # --- Crop ---
    if args.crop:
        l, t, r, b = args.crop
        w, h = img.size
        l, t = max(0, l), max(0, t)
        r, b = min(w, r), min(h, b)
        if r > l and b > t:
            img = img.crop((l, t, r, b))
        else:
            print("Aviso: coordenadas de crop inválidas — ignorado.", file=sys.stderr)

    # --- Rotate ---
    if args.rotate is not None:
        fill = get_fill_color(img)
        img = img.rotate(args.rotate, expand=True, fillcolor=fill)

    # --- Flip ---
    if args.flip == "horizontal":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif args.flip == "vertical":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

    return img


def save_image(img: Image.Image, out_path: Path, fmt: str, quality: int):
    """Salva imagem no formato e qualidade especificados."""
    pil_format = FORMAT_MAP.get(fmt.lower(), fmt.upper()) if fmt else None

    # Normalizar a partir da extensão se fmt não fornecido
    if pil_format is None:
        pil_format = FORMAT_MAP.get(out_path.suffix.lstrip(".").lower(), "JPEG")

    # JPEG não suporta transparência
    if pil_format == "JPEG":
        img = prepare_for_jpeg(img)

    save_kwargs = {}
    if pil_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), format=pil_format, **save_kwargs)


def process_file(input_path: Path, args) -> Path:
    """Processa um único arquivo. Retorna o caminho de saída."""
    img = Image.open(input_path)

    # Respeitar orientação EXIF
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    original_size = input_path.stat().st_size
    original_dims = img.size

    img = apply_transforms(img, args)

    out_path, backup_path = determine_paths(input_path, args)

    # Fazer backup antes de sobrescrever
    if backup_path and not backup_path.exists():
        input_path.rename(backup_path)

    save_image(img, out_path, args.format, args.quality)

    new_size = out_path.stat().st_size
    size_diff = ((new_size - original_size) / original_size * 100) if original_size else 0
    sign = "+" if size_diff >= 0 else ""
    print(
        f"✓ {input_path.name} → {out_path.name}  "
        f"{original_dims[0]}x{original_dims[1]} → {img.size[0]}x{img.size[1]}  "
        f"{original_size // 1024}KB → {new_size // 1024}KB ({sign}{size_diff:.0f}%)"
    )
    return out_path


def get_image_files(directory: Path):
    return sorted(
        f for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_INPUT
    )


def main():
    parser = argparse.ArgumentParser(
        description="Transformar imagens: resize, rotate, flip, crop, convert.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  transform.py foto.jpg --rotate 90
  transform.py foto.jpg --fit-width 1200 --format webp
  transform.py foto.jpg --flip horizontal --suffix _mirror
  transform.py fotos/ --scale 50 --batch --suffix _small
  transform.py foto.jpg --crop 0,0,800,600 --rotate 90 --format png
""",
    )

    parser.add_argument("input", help="Arquivo de imagem ou diretório (com --batch)")

    # Resize (mutuamente exclusivos)
    resize_group = parser.add_mutually_exclusive_group()
    resize_group.add_argument(
        "--resize", type=parse_resize, metavar="WxH",
        help="Redimensionar para dimensões exatas (ex: 800x600)",
    )
    resize_group.add_argument(
        "--scale", type=float, metavar="N",
        help="Escalar por porcentagem (ex: 50 = 50%%)",
    )
    resize_group.add_argument(
        "--fit-width", type=int, metavar="N",
        help="Ajustar largura mantendo proporção",
    )
    resize_group.add_argument(
        "--fit-height", type=int, metavar="N",
        help="Ajustar altura mantendo proporção",
    )

    # Outras transformações
    parser.add_argument(
        "--rotate", type=float, metavar="GRAUS",
        help="Rotacionar N graus anti-horário (ex: 90, 180, 270, -90, 45)",
    )
    parser.add_argument(
        "--flip", choices=["horizontal", "vertical"],
        help="Espelhar: horizontal ou vertical",
    )
    parser.add_argument(
        "--crop", type=parse_crop, metavar="L,T,R,B",
        help="Recortar (esquerda,topo,direita,base em pixels)",
    )

    # Formato e qualidade
    parser.add_argument(
        "--format", choices=list(FORMAT_MAP.keys()), metavar="EXT",
        help="Converter formato de saída: jpg, png, webp, gif, bmp, tiff",
    )
    parser.add_argument(
        "--quality", type=int, default=85, metavar="N",
        help="Qualidade JPG/WebP 1-95 (padrão: 85)",
    )

    # Opções de saída
    parser.add_argument(
        "--output", "-o", metavar="CAMINHO",
        help="Arquivo ou diretório de saída (preserva original)",
    )
    parser.add_argument(
        "--suffix", metavar="TEXTO",
        help="Sufixo no nome do arquivo de saída (ex: _thumb — preserva original)",
    )
    parser.add_argument(
        "--no-backup", action="store_true",
        help="Sobrescrever original sem criar backup",
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="Processar todos os arquivos de imagem em um diretório",
    )

    args = parser.parse_args()

    input_path = Path(args.input).expanduser()

    if not input_path.exists():
        print(f"Erro: '{input_path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    # Coletar arquivos
    if args.batch or input_path.is_dir():
        if not input_path.is_dir():
            print("Erro: --batch requer um diretório.", file=sys.stderr)
            sys.exit(1)
        files = get_image_files(input_path)
        if not files:
            print(f"Nenhuma imagem encontrada em '{input_path}'.", file=sys.stderr)
            sys.exit(1)
    else:
        if input_path.suffix.lower() not in SUPPORTED_INPUT:
            print(
                f"Aviso: extensão '{input_path.suffix}' pode não ser suportada.",
                file=sys.stderr,
            )
        files = [input_path]

    # Processar
    errors = []
    for f in files:
        try:
            process_file(f, args)
        except Exception as e:
            errors.append((f, str(e)))
            print(f"✗ {f.name}: {e}", file=sys.stderr)

    total = len(files)
    if errors:
        print(f"\n{len(errors)}/{total} arquivo(s) com erro.", file=sys.stderr)
        sys.exit(1)
    else:
        if total > 1:
            print(f"\n{total} arquivo(s) processado(s) com sucesso.")


if __name__ == "__main__":
    main()
