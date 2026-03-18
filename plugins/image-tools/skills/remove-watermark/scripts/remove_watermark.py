#!/usr/bin/env python3
"""
Remove marcas d'água de imagens (especialmente de geradores de IA).
Usa OpenCV inpainting para preencher a região da marca d'água com o conteúdo ao redor.

Sem argumento de saída, renomeia a original para _original (com marca d'água) e salva a
imagem limpa com o nome original.

Uso:
  python remove_watermark.py entrada.png
  python remove_watermark.py entrada.png -c br -s 8
  python remove_watermark.py entrada.png saida.png
  python remove_watermark.py entrada.png --rect 700,450,800,500
  python remove_watermark.py pasta_entrada/
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np


def resolve_output_path(input_path: str) -> str:
    """Resolve caminho de saída quando não especificado.

    Renomeia a imagem original para nome_original.ext (cmd = com marca d'água)
    e retorna o caminho original para salvar a imagem limpa.
    Se o arquivo já contém _original no nome, não adiciona novamente.

    @param input_path: caminho da imagem de entrada
    @returns: caminho onde salvar a imagem limpa
    """
    p = Path(input_path)
    stem = p.stem
    suffix = p.suffix

    # Se já tem _original, a original com marca d'água já foi preservada antes
    if stem.endswith("_original"):
        # Saída é o nome sem _original
        clean_name = stem[:-4] + suffix
        return str(p.parent / clean_name)

    # Renomear original para _original
    cmd_path = p.parent / f"{stem}_original{suffix}"
    p.rename(cmd_path)
    print(f"Original renomeada: {cmd_path}")

    # A imagem limpa fica com o nome original
    return str(input_path)


def remove_watermark(
    input_path: str,
    output_path: str,
    corner: str = "br",
    size_pct: int = 8,
    padding: int = 10,
    radius: int = 5,
    rect: str | None = None,
    feather: int = 15,
) -> None:
    """Remove marca d'água de uma imagem via inpainting.

    @param input_path: caminho da imagem de entrada
    @param output_path: caminho da imagem de saída
    @param corner: canto da marca d'água (br, bl, tr, tl)
    @param size_pct: tamanho da região em porcentagem da imagem
    @param padding: padding extra em pixels ao redor da região
    @param radius: raio do inpainting (pixels)
    @param rect: região manual "x1,y1,x2,y2" (ignora corner/size_pct)
    @param feather: suavização da borda da máscara (evita corte abrupto)
    """
    # Se o arquivo original foi renomeado para _original (resolve_output_path),
    # ler a partir do arquivo _original
    read_path = Path(input_path)
    if not read_path.exists():
        cmd_candidate = read_path.parent / f"{read_path.stem}_original{read_path.suffix}"
        if cmd_candidate.exists():
            read_path = cmd_candidate

    img = cv2.imread(str(read_path), cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Erro: não foi possível abrir '{read_path}'", file=sys.stderr)
        sys.exit(1)

    h, w = img.shape[:2]

    if rect:
        coords = [int(x.strip()) for x in rect.split(",")]
        if len(coords) != 4:
            print("Erro: --rect deve ter 4 valores: x1,y1,x2,y2", file=sys.stderr)
            sys.exit(1)
        x1, y1, x2, y2 = coords
    else:
        region_w = int(w * size_pct / 100)
        region_h = int(h * size_pct / 100)

        corners = {
            "br": (w - region_w, h - region_h, w, h),
            "bl": (0, h - region_h, region_w, h),
            "tr": (w - region_w, 0, w, region_h),
            "tl": (0, 0, region_w, region_h),
        }

        if corner not in corners:
            print(f"Erro: canto inválido '{corner}'. Use: br, bl, tr, tl", file=sys.stderr)
            sys.exit(1)

        x1, y1, x2, y2 = corners[corner]

    # Aplicar padding
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(w, x2 + padding)
    y2 = min(h, y2 + padding)

    # Converter para BGR se tiver canal alpha
    if len(img.shape) == 3 and img.shape[2] == 4:
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    else:
        img_bgr = img

    # Criar máscara com feathering (transição suave nas bordas)
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255

    if feather > 0:
        mask = cv2.GaussianBlur(mask, (0, 0), feather)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Inpainting (Telea = melhor para texturas, NS = melhor para bordas definidas)
    result = cv2.inpaint(img_bgr, mask, radius, cv2.INPAINT_TELEA)

    # Garantir diretório de saída existe
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(output_path), result)
    print(f"OK: {output_path}")


def process_batch(input_dir: str, output_dir: str, **kwargs) -> None:
    """Processa todas as imagens de uma pasta.

    @param input_dir: pasta com imagens de entrada
    @param output_dir: pasta para salvar resultados
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
    images = [f for f in input_path.iterdir() if f.suffix.lower() in extensions]

    if not images:
        print(f"Nenhuma imagem encontrada em '{input_dir}'", file=sys.stderr)
        sys.exit(1)

    in_place = input_path == output_path
    print(f"Processando {len(images)} imagens...")
    for img_file in sorted(images):
        if in_place:
            out_file = resolve_output_path(str(img_file))
        else:
            out_file = str(output_path / img_file.name)
        remove_watermark(str(img_file), out_file, **kwargs)

    print(f"Concluído: {len(images)} imagens processadas em '{output_dir}'")


def main():
    parser = argparse.ArgumentParser(
        description="Remove marca d'água de imagens de geradores de IA"
    )
    parser.add_argument("input", help="Imagem ou pasta de entrada")
    parser.add_argument("output", nargs="?", default=None,
                        help="Imagem ou pasta de saída (opcional: sem informar, "
                             "renomeia original para _original e salva limpa no nome original)")
    parser.add_argument(
        "-c", "--corner", default="br",
        choices=["br", "bl", "tr", "tl"],
        help="Canto da marca d'água: br=inferior-direito, bl=inferior-esquerdo, "
             "tr=superior-direito, tl=superior-esquerdo (padrão: br)"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=8,
        help="Tamanho da região em %% da imagem (padrão: 8)"
    )
    parser.add_argument(
        "-p", "--padding", type=int, default=10,
        help="Padding extra em pixels (padrão: 10)"
    )
    parser.add_argument(
        "-r", "--radius", type=int, default=5,
        help="Raio do inpainting em pixels (padrão: 5)"
    )
    parser.add_argument(
        "--rect", type=str, default=None,
        help="Região manual: x1,y1,x2,y2 em pixels (ignora --corner e --size)"
    )
    parser.add_argument(
        "-f", "--feather", type=int, default=15,
        help="Suavização da borda da máscara (padrão: 15)"
    )

    args = parser.parse_args()
    input_path = Path(args.input)

    kwargs = dict(
        corner=args.corner,
        size_pct=args.size,
        padding=args.padding,
        radius=args.radius,
        rect=args.rect,
        feather=args.feather,
    )

    if input_path.is_dir():
        output_dir = args.output or str(input_path)
        process_batch(args.input, output_dir, **kwargs)
    else:
        output = args.output or resolve_output_path(args.input)
        remove_watermark(args.input, output, **kwargs)


if __name__ == "__main__":
    main()
