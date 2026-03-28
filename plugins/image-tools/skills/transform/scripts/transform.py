#!/usr/bin/env python3
"""
Image Transform Tool
Redimensionar, rotacionar, espelhar, recortar, ajustar e converter imagens com Pillow.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
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


def parse_pad(value):
    """Aceita N (uniforme) ou T,R,B,L (individual)."""
    parts = value.split(",")
    if len(parts) == 1:
        n = int(parts[0])
        return (n, n, n, n)
    elif len(parts) == 4:
        return tuple(int(p.strip()) for p in parts)
    else:
        raise argparse.ArgumentTypeError(
            f"Formato inválido: '{value}'. Use N (uniforme) ou T,R,B,L"
        )


def parse_color(value):
    """Aceita nomes de cor ou hex (#RRGGBB / #RGB)."""
    color_names = {
        "white": (255, 255, 255), "black": (0, 0, 0),
        "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255),
        "transparent": (0, 0, 0, 0),
    }
    lower = value.lower().strip()
    if lower in color_names:
        return color_names[lower]
    if lower.startswith("#"):
        h = lower.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        if len(h) == 8:
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    raise argparse.ArgumentTypeError(
        f"Cor inválida: '{value}'. Use nome (white, black...) ou hex (#RRGGBB)"
    )


def determine_paths(input_path: Path, args):
    """
    Retorna (output_path, backup_path_or_None).
    - Se --output: salva no destino, sem backup.
    - Se --suffix: salva com sufixo, sem backup.
    - Caso contrário (in-place): renomeia original para _original, salva no nome original.
    - Se --no-backup: in-place sem backup.
    """
    input_ext = input_path.suffix
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

    stem = input_path.stem
    if stem.endswith("_original"):
        return out_file, None

    backup_path = input_path.parent / (stem + "_original" + input_ext)
    return out_file, backup_path


def get_fill_color(img: Image.Image):
    """Retorna cor de preenchimento adequada ao modo da imagem."""
    if img.mode in ("RGBA", "LA"):
        return (0, 0, 0, 0)
    if img.mode == "RGB":
        return (255, 255, 255)
    return None


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


def apply_trim(img: Image.Image, fuzz: int = 10) -> Image.Image:
    """Remove bordas uniformes ao redor da imagem.

    Detecta a cor predominante nos cantos e remove qualquer borda contínua
    dessa cor (com tolerância definida por fuzz).
    """
    import numpy as np

    arr = np.array(img)
    if arr.ndim == 2:
        arr = arr[:, :, np.newaxis]

    # Detectar cor de fundo a partir dos 4 cantos
    corners = [arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1]]
    bg = np.median(corners, axis=0).astype(np.uint8)

    # Máscara de pixels diferentes do fundo
    diff = np.abs(arr.astype(int) - bg.astype(int)).max(axis=-1)
    mask = diff > fuzz

    # Encontrar bounding box do conteúdo
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)

    if not rows.any() or not cols.any():
        return img  # Imagem inteira é fundo — retorna sem alterar

    top = np.argmax(rows)
    bottom = len(rows) - np.argmax(rows[::-1])
    left = np.argmax(cols)
    right = len(cols) - np.argmax(cols[::-1])

    return img.crop((left, top, right, bottom))


def apply_pad(img: Image.Image, padding: tuple, color) -> Image.Image:
    """Adiciona padding ao redor da imagem.

    padding: (top, right, bottom, left)
    """
    top, right, bottom, left = padding
    new_w = img.width + left + right
    new_h = img.height + top + bottom

    # Ajustar cor para o modo da imagem
    if img.mode == "RGBA" and isinstance(color, tuple) and len(color) == 3:
        color = color + (255,)
    elif img.mode == "RGB" and isinstance(color, tuple) and len(color) == 4:
        color = color[:3]

    new_img = Image.new(img.mode, (new_w, new_h), color)
    new_img.paste(img, (left, top))
    return new_img


def apply_transforms(img: Image.Image, args) -> Image.Image:
    """Aplica todas as transformações na ordem:
    trim → resize → crop → pad → rotate → flip → adjustments → filters.
    """

    # --- Trim ---
    if args.trim:
        img = apply_trim(img, fuzz=args.trim_fuzz)

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

    # --- Pad ---
    if args.pad:
        color = args.pad_color if args.pad_color else (255, 255, 255)
        img = apply_pad(img, args.pad, color)

    # --- Rotate ---
    if args.rotate is not None:
        fill = get_fill_color(img)
        img = img.rotate(args.rotate, expand=True, fillcolor=fill)

    # --- Flip ---
    if args.flip == "horizontal":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif args.flip == "vertical":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

    # --- Ajustes visuais ---
    if args.brightness is not None:
        img = ImageEnhance.Brightness(img).enhance(args.brightness)

    if args.contrast is not None:
        img = ImageEnhance.Contrast(img).enhance(args.contrast)

    if args.saturation is not None:
        img = ImageEnhance.Color(img).enhance(args.saturation)

    if args.grayscale:
        img = ImageOps.grayscale(img)

    # --- Filtros ---
    if args.sharpen:
        img = img.filter(ImageFilter.SHARPEN)

    if args.blur is not None:
        img = img.filter(ImageFilter.GaussianBlur(radius=args.blur))

    return img


def save_image(img: Image.Image, out_path: Path, fmt: str, quality: int):
    """Salva imagem no formato e qualidade especificados."""
    pil_format = FORMAT_MAP.get(fmt.lower(), fmt.upper()) if fmt else None

    if pil_format is None:
        pil_format = FORMAT_MAP.get(out_path.suffix.lstrip(".").lower(), "JPEG")

    if pil_format == "JPEG":
        img = prepare_for_jpeg(img)

    save_kwargs = {}
    if pil_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), format=pil_format, **save_kwargs)


def show_info(input_path: Path):
    """Mostra informações detalhadas da imagem em formato JSON."""
    img = Image.open(input_path)

    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    file_size = input_path.stat().st_size
    info = {
        "file": str(input_path),
        "format": img.format or input_path.suffix.lstrip(".").upper(),
        "mode": img.mode,
        "width": img.width,
        "height": img.height,
        "file_size_bytes": file_size,
        "file_size_human": f"{file_size / 1024:.1f}KB" if file_size < 1024 * 1024
                           else f"{file_size / (1024 * 1024):.1f}MB",
    }

    # DPI se disponível
    dpi = img.info.get("dpi")
    if dpi:
        info["dpi"] = {"x": round(dpi[0]), "y": round(dpi[1])}

    # Frames (GIF animado)
    try:
        n_frames = getattr(img, "n_frames", 1)
        if n_frames > 1:
            info["frames"] = n_frames
    except Exception:
        pass

    print(json.dumps(info, indent=2, ensure_ascii=False))


def process_file(input_path: Path, args) -> Path:
    """Processa um único arquivo. Retorna o caminho de saída."""
    img = Image.open(input_path)

    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    original_size = input_path.stat().st_size
    original_dims = img.size

    img = apply_transforms(img, args)

    out_path, backup_path = determine_paths(input_path, args)

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
        description="Transformar imagens: resize, rotate, flip, crop, trim, pad, adjust, convert.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  transform.py foto.jpg --rotate 90
  transform.py foto.jpg --fit-width 1200 --format webp
  transform.py foto.jpg --trim --resize 800x600 --sharpen
  transform.py foto.jpg --brightness 1.2 --contrast 1.1 --suffix _enhanced
  transform.py foto.jpg --pad 20 --pad-color "#f0f0f0"
  transform.py foto.jpg --info
  transform.py fotos/ --scale 50 --batch --suffix _small
""",
    )

    parser.add_argument("input", help="Arquivo de imagem ou diretório (com --batch)")

    # Info (exibe e sai)
    parser.add_argument(
        "--info", action="store_true",
        help="Exibir informações da imagem (dimensões, formato, tamanho, DPI)",
    )

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

    # Transformações geométricas
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

    # Trim e Padding
    parser.add_argument(
        "--trim", action="store_true",
        help="Remover bordas/margens uniformes automaticamente",
    )
    parser.add_argument(
        "--trim-fuzz", type=int, default=10, metavar="N",
        help="Tolerância para trim (0-255, padrão: 10)",
    )
    parser.add_argument(
        "--pad", type=parse_pad, metavar="N ou T,R,B,L",
        help="Adicionar padding (uniforme ou individual)",
    )
    parser.add_argument(
        "--pad-color", type=parse_color, metavar="COR",
        help="Cor do padding: nome (white, black) ou hex (#RRGGBB). Padrão: white",
    )

    # Ajustes visuais
    parser.add_argument(
        "--brightness", type=float, metavar="F",
        help="Fator de brilho (1.0=original, >1=mais claro, <1=mais escuro)",
    )
    parser.add_argument(
        "--contrast", type=float, metavar="F",
        help="Fator de contraste (1.0=original, >1=mais contraste)",
    )
    parser.add_argument(
        "--saturation", type=float, metavar="F",
        help="Fator de saturação (1.0=original, 0=cinza, >1=mais vibrante)",
    )
    parser.add_argument(
        "--grayscale", action="store_true",
        help="Converter para escala de cinza",
    )

    # Filtros
    parser.add_argument(
        "--sharpen", action="store_true",
        help="Aumentar nitidez da imagem",
    )
    parser.add_argument(
        "--blur", type=float, metavar="R",
        help="Desfoque gaussiano com raio R (ex: 2.0)",
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

    # Modo info: exibe e sai
    if args.info:
        if input_path.is_dir():
            for f in get_image_files(input_path):
                show_info(f)
                print()
        else:
            show_info(input_path)
        return

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
