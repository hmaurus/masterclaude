#!/usr/bin/env python3
"""
Image Split Tool
Dividir imagens em partes: grid, faixas horizontais/verticais, auto-detecção de elementos.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    print("Erro: Pillow não instalado. Execute setup.sh primeiro.", file=sys.stderr)
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("Erro: numpy não instalado. Execute setup.sh primeiro.", file=sys.stderr)
    sys.exit(1)

SUPPORTED_INPUT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".tif"}
FORMAT_MAP = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP",
              "gif": "GIF", "bmp": "BMP", "tiff": "TIFF"}


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


def save_piece(img: Image.Image, path: Path, fmt: str = None, quality: int = 85):
    """Salva um pedaço da imagem no formato e qualidade especificados."""
    if fmt:
        pil_format = FORMAT_MAP.get(fmt.lower(), fmt.upper())
    else:
        pil_format = FORMAT_MAP.get(path.suffix.lstrip(".").lower(), "PNG")

    if pil_format == "JPEG":
        img = prepare_for_jpeg(img)

    save_kwargs = {}
    if pil_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(path), format=pil_format, **save_kwargs)


def get_output_dir(input_path: Path, output: str = None) -> Path:
    """Determina o diretório de saída para os pedaços."""
    if output:
        out = Path(output).expanduser()
        out.mkdir(parents=True, exist_ok=True)
        return out
    # Cria subpasta ao lado do arquivo original com nome do arquivo
    out = input_path.parent / f"{input_path.stem}_split"
    out.mkdir(parents=True, exist_ok=True)
    return out


def get_output_ext(input_path: Path, fmt: str = None) -> str:
    """Retorna a extensão do arquivo de saída."""
    if fmt:
        return "." + fmt.lower().replace("jpeg", "jpg")
    return input_path.suffix


def split_grid(img: Image.Image, cols: int, rows: int) -> list:
    """Divide imagem em grade CxR. Retorna lista de (imagem, nome)."""
    w, h = img.size
    cell_w = w / cols
    cell_h = h / rows

    pieces = []
    for r in range(rows):
        for c in range(cols):
            left = int(c * cell_w)
            top = int(r * cell_h)
            right = int((c + 1) * cell_w) if c < cols - 1 else w
            bottom = int((r + 1) * cell_h) if r < rows - 1 else h
            piece = img.crop((left, top, right, bottom))
            name = f"r{r+1}_c{c+1}"
            pieces.append((piece, name))

    return pieces


def split_horizontal(img: Image.Image, n: int) -> list:
    """Divide imagem em N faixas horizontais (cortes de cima para baixo)."""
    w, h = img.size
    strip_h = h / n

    pieces = []
    for i in range(n):
        top = int(i * strip_h)
        bottom = int((i + 1) * strip_h) if i < n - 1 else h
        piece = img.crop((0, top, w, bottom))
        pieces.append((piece, f"strip_{i+1}"))

    return pieces


def split_vertical(img: Image.Image, n: int) -> list:
    """Divide imagem em N faixas verticais (cortes da esquerda para direita)."""
    w, h = img.size
    strip_w = w / n

    pieces = []
    for i in range(n):
        left = int(i * strip_w)
        right = int((i + 1) * strip_w) if i < n - 1 else w
        piece = img.crop((left, 0, right, h))
        pieces.append((piece, f"col_{i+1}"))

    return pieces


def detect_background_color(arr: np.ndarray) -> np.ndarray:
    """Detecta cor de fundo a partir dos cantos da imagem.

    Amostra uma faixa de 5% em cada borda e calcula a mediana.
    Mais robusto do que olhar só 4 pixels.
    """
    h, w = arr.shape[:2]
    margin_y = max(1, h // 20)
    margin_x = max(1, w // 20)

    # Amostrar pixels das bordas
    top = arr[:margin_y, :].reshape(-1, arr.shape[-1]) if arr.ndim == 3 else arr[:margin_y, :].ravel()
    bottom = arr[-margin_y:, :].reshape(-1, arr.shape[-1]) if arr.ndim == 3 else arr[-margin_y:, :].ravel()
    left = arr[:, :margin_x].reshape(-1, arr.shape[-1]) if arr.ndim == 3 else arr[:, :margin_x].ravel()
    right = arr[:, -margin_x:].reshape(-1, arr.shape[-1]) if arr.ndim == 3 else arr[:, -margin_x:].ravel()

    if arr.ndim == 3:
        border_pixels = np.concatenate([top, bottom, left, right], axis=0)
    else:
        border_pixels = np.concatenate([top, bottom, left, right])

    return np.median(border_pixels, axis=0).astype(np.uint8)


def auto_split_opencv(img: Image.Image, min_size: int, padding: int, fuzz: int) -> list:
    """Auto-split usando OpenCV contour detection (mais robusto)."""
    import cv2

    arr = np.array(img)

    # Converter para grayscale para detecção
    if arr.ndim == 3 and arr.shape[2] >= 3:
        gray = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2GRAY)
    else:
        gray = arr if arr.ndim == 2 else arr[:, :, 0]

    # Detectar cor de fundo
    bg_val = int(np.median([gray[0, 0], gray[0, -1], gray[-1, 0], gray[-1, -1]]))

    # Criar máscara binária (foreground = branco)
    if bg_val > 127:
        _, binary = cv2.threshold(gray, max(0, bg_val - fuzz), 255, cv2.THRESH_BINARY_INV)
    else:
        _, binary = cv2.threshold(gray, min(255, bg_val + fuzz), 255, cv2.THRESH_BINARY)

    # Operações morfológicas para conectar componentes próximos e remover ruído
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    # Encontrar contornos
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extrair bounding boxes, filtrar por tamanho mínimo
    boxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w >= min_size and h >= min_size:
            boxes.append((x, y, x + w, y + h))

    # Ordenar: cima para baixo, esquerda para direita
    boxes.sort(key=lambda b: (b[1] // (img.height // 10 + 1), b[0]))

    # Extrair pedaços com padding
    pieces = []
    img_w, img_h = img.size
    for i, (x1, y1, x2, y2) in enumerate(boxes):
        left = max(0, x1 - padding)
        top = max(0, y1 - padding)
        right = min(img_w, x2 + padding)
        bottom = min(img_h, y2 + padding)
        piece = img.crop((left, top, right, bottom))
        pieces.append((piece, f"element_{i+1}"))

    return pieces


def auto_split_projection(img: Image.Image, min_size: int, padding: int, fuzz: int) -> list:
    """Auto-split usando projeção (fallback sem OpenCV).

    Projeta a máscara de foreground nos eixos X e Y para encontrar
    regiões separadas por gaps de background.
    """
    arr = np.array(img)

    # Converter para grayscale
    if arr.ndim == 3:
        # Weighted grayscale
        gray = np.dot(arr[:, :, :3].astype(float), [0.299, 0.587, 0.114])
    else:
        gray = arr.astype(float)

    # Detectar cor de fundo
    bg = detect_background_color(gray[:, :, np.newaxis] if gray.ndim == 2 else arr)
    bg_val = float(bg[0]) if bg.ndim > 0 and len(bg) > 0 else float(bg)

    # Criar máscara
    diff = np.abs(gray - bg_val)
    mask = diff > fuzz

    # Projeção no eixo Y (soma de foreground por linha)
    row_proj = np.any(mask, axis=1)
    # Projeção no eixo X (soma de foreground por coluna)
    col_proj = np.any(mask, axis=0)

    def find_segments(proj, min_len):
        """Encontra segmentos contínuos de True na projeção."""
        segments = []
        in_segment = False
        start = 0
        for i, val in enumerate(proj):
            if val and not in_segment:
                start = i
                in_segment = True
            elif not val and in_segment:
                if i - start >= min_len:
                    segments.append((start, i))
                in_segment = False
        if in_segment and len(proj) - start >= min_len:
            segments.append((start, len(proj)))
        return segments

    row_segs = find_segments(row_proj, min_size)
    col_segs = find_segments(col_proj, min_size)

    if not row_segs or not col_segs:
        return []

    # Se há múltiplos segmentos em ambos os eixos, criar grade
    # Se só um eixo tem múltiplos, dividir nesse eixo
    pieces = []
    img_w, img_h = img.size
    idx = 0

    if len(row_segs) > 1 and len(col_segs) > 1:
        # Grade: cada interseção é um elemento
        for r_start, r_end in row_segs:
            for c_start, c_end in col_segs:
                # Verificar se tem conteúdo nesta célula
                cell_mask = mask[r_start:r_end, c_start:c_end]
                if np.any(cell_mask):
                    left = max(0, c_start - padding)
                    top = max(0, r_start - padding)
                    right = min(img_w, c_end + padding)
                    bottom = min(img_h, r_end + padding)
                    piece = img.crop((left, top, right, bottom))
                    idx += 1
                    pieces.append((piece, f"element_{idx}"))
    elif len(row_segs) > 1:
        # Dividir só por linhas
        for r_start, r_end in row_segs:
            left = max(0, col_segs[0][0] - padding)
            top = max(0, r_start - padding)
            right = min(img_w, col_segs[-1][1] + padding)
            bottom = min(img_h, r_end + padding)
            piece = img.crop((left, top, right, bottom))
            idx += 1
            pieces.append((piece, f"element_{idx}"))
    elif len(col_segs) > 1:
        # Dividir só por colunas
        for c_start, c_end in col_segs:
            left = max(0, c_start - padding)
            top = max(0, row_segs[0][0] - padding)
            right = min(img_w, c_end + padding)
            bottom = min(img_h, row_segs[-1][1] + padding)
            piece = img.crop((left, top, right, bottom))
            idx += 1
            pieces.append((piece, f"element_{idx}"))
    else:
        # Apenas um bloco
        r_start, r_end = row_segs[0]
        c_start, c_end = col_segs[0]
        left = max(0, c_start - padding)
        top = max(0, r_start - padding)
        right = min(img_w, c_end + padding)
        bottom = min(img_h, r_end + padding)
        piece = img.crop((left, top, right, bottom))
        pieces.append((piece, "element_1"))

    return pieces


def auto_split(img: Image.Image, min_size: int, padding: int, fuzz: int) -> list:
    """Auto-detecta elementos em fundo uniforme e extrai cada um.

    Usa OpenCV se disponível (contour detection — mais robusto para
    formas irregulares e overlapping). Fallback para projeção com numpy
    (funciona bem para layouts em grade/coluna/linha).
    """
    try:
        import cv2  # noqa: F401
        method = "opencv"
        pieces = auto_split_opencv(img, min_size, padding, fuzz)
    except ImportError:
        method = "projection"
        pieces = auto_split_projection(img, min_size, padding, fuzz)

    if not pieces:
        print("Nenhum elemento detectado. Tente ajustar --min-size ou --fuzz.", file=sys.stderr)
    else:
        print(f"Método: {method} | {len(pieces)} elemento(s) detectado(s)")

    return pieces


def parse_grid(value):
    """Parse CxR grid spec."""
    parts = value.lower().split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            f"Formato inválido: '{value}'. Use CxR (ex: 3x2 = 3 colunas × 2 linhas)"
        )
    try:
        cols, rows = int(parts[0]), int(parts[1])
        if cols < 1 or rows < 1:
            raise ValueError()
        return cols, rows
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Valores devem ser inteiros positivos: '{value}'"
        )


def process_file(input_path: Path, args):
    """Processa um único arquivo de imagem."""
    img = Image.open(input_path)

    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    print(f"Entrada: {input_path.name} ({img.width}x{img.height})")

    # Determinar operação
    if args.grid:
        cols, rows = args.grid
        pieces = split_grid(img, cols, rows)
        op_name = f"grid {cols}x{rows}"
    elif args.split_h:
        pieces = split_horizontal(img, args.split_h)
        op_name = f"horizontal ÷{args.split_h}"
    elif args.split_v:
        pieces = split_vertical(img, args.split_v)
        op_name = f"vertical ÷{args.split_v}"
    elif args.auto_split:
        pieces = auto_split(img, args.min_size, args.split_padding, args.fuzz)
        op_name = "auto-split"
    else:
        print("Erro: especifique uma operação (--grid, --split-h, --split-v, --auto-split)", file=sys.stderr)
        sys.exit(1)

    if not pieces:
        return

    # Salvar pedaços
    out_dir = get_output_dir(input_path, args.output)
    ext = get_output_ext(input_path, args.format)
    prefix = args.prefix or input_path.stem

    saved = []
    for piece_img, piece_name in pieces:
        filename = f"{prefix}_{piece_name}{ext}"
        out_path = out_dir / filename
        save_piece(piece_img, out_path, args.format, args.quality)
        saved.append({
            "file": str(out_path),
            "size": f"{piece_img.width}x{piece_img.height}",
        })

    print(f"Operação: {op_name}")
    print(f"Saída: {out_dir}/")
    print(f"Arquivos: {len(saved)}")
    for s in saved:
        print(f"  ✓ {Path(s['file']).name} ({s['size']})")

    # Salvar manifesto JSON para referência
    manifest = {
        "source": str(input_path),
        "operation": op_name,
        "output_dir": str(out_dir),
        "pieces": saved,
    }
    manifest_path = out_dir / "_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Dividir imagens: grid, faixas horizontais/verticais, auto-detecção de elementos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  split.py sprite.png --grid 4x3
  split.py banner.jpg --split-h 3
  split.py icons.png --auto-split --min-size 30
  split.py collage.jpg --split-v 2 --output ~/pedacos/
""",
    )

    parser.add_argument("input", help="Arquivo de imagem para dividir")

    # Operações de split (mutuamente exclusivas)
    split_group = parser.add_mutually_exclusive_group(required=True)
    split_group.add_argument(
        "--grid", type=parse_grid, metavar="CxR",
        help="Dividir em grade (Colunas × Linhas). Ex: 3x2 = 6 pedaços",
    )
    split_group.add_argument(
        "--split-h", type=int, metavar="N",
        help="Dividir em N faixas horizontais iguais (corte de cima para baixo)",
    )
    split_group.add_argument(
        "--split-v", type=int, metavar="N",
        help="Dividir em N faixas verticais iguais (corte da esquerda para direita)",
    )
    split_group.add_argument(
        "--auto-split", action="store_true",
        help="Detectar e extrair elementos automaticamente (fundo uniforme)",
    )

    # Opções de auto-split
    parser.add_argument(
        "--min-size", type=int, default=50, metavar="N",
        help="Tamanho mínimo (pixels) para considerar como elemento no auto-split (padrão: 50)",
    )
    parser.add_argument(
        "--split-padding", type=int, default=5, metavar="N",
        help="Margem em pixels ao redor de cada elemento extraído (padrão: 5)",
    )
    parser.add_argument(
        "--fuzz", type=int, default=30, metavar="N",
        help="Tolerância para detecção de fundo (0-255, padrão: 30)",
    )

    # Saída
    parser.add_argument(
        "--output", "-o", metavar="DIR",
        help="Diretório de saída (padrão: <nome>_split/ ao lado do original)",
    )
    parser.add_argument(
        "--prefix", metavar="TEXTO",
        help="Prefixo para nomes dos arquivos (padrão: nome do arquivo original)",
    )
    parser.add_argument(
        "--format", choices=["jpg", "jpeg", "png", "webp", "bmp", "tiff"], metavar="EXT",
        help="Formato de saída (padrão: mesmo do original)",
    )
    parser.add_argument(
        "--quality", type=int, default=85, metavar="N",
        help="Qualidade JPG/WebP (1-95, padrão: 85)",
    )

    args = parser.parse_args()

    input_path = Path(args.input).expanduser()

    if not input_path.exists():
        print(f"Erro: '{input_path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_file():
        print("Erro: input deve ser um arquivo de imagem, não diretório.", file=sys.stderr)
        sys.exit(1)

    if input_path.suffix.lower() not in SUPPORTED_INPUT:
        print(f"Aviso: extensão '{input_path.suffix}' pode não ser suportada.", file=sys.stderr)

    process_file(input_path, args)


if __name__ == "__main__":
    main()
