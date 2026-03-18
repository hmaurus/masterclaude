#!/usr/bin/env python3
"""
Remove background de imagens usando rembg.
Wrapper que adiciona saída automática: renomeia a original para _original e salva
a imagem sem fundo com o nome original.

Uso:
  python remove_bg.py foto.png
  python remove_bg.py foto.png saida.png
  python remove_bg.py foto.png -m u2net_human_seg
  python remove_bg.py pasta/
"""

import argparse
import subprocess
import sys
from pathlib import Path

REMBG_BIN = Path.home() / "venvs" / "rembg" / "bin" / "rembg"
SUFFIX = "_original"


def resolve_output_path(input_path: str) -> str:
    """Resolve caminho de saída quando não especificado.

    Renomeia a imagem original para nome_original.ext e retorna o caminho
    original para salvar a imagem processada.
    Se o arquivo já contém _original no nome, não adiciona novamente.

    @param input_path: caminho da imagem de entrada
    @returns: caminho onde salvar a imagem processada
    """
    p = Path(input_path)
    stem = p.stem
    suffix = p.suffix

    if stem.endswith(SUFFIX):
        clean_name = stem[: -len(SUFFIX)] + ".png"
        return str(p.parent / clean_name)

    original_path = p.parent / f"{stem}{SUFFIX}{suffix}"
    p.rename(original_path)
    print(f"Original renomeada: {original_path}")

    # Saída sempre em PNG (transparência)
    output_name = f"{stem}.png"
    return str(p.parent / output_name)


def run_rembg(input_path: str, output_path: str, model: str | None = None,
              alpha_matting: bool = False, ae: int = 10, ab: int = 10) -> None:
    """Executa rembg para remover background.

    @param input_path: caminho da imagem de entrada
    @param output_path: caminho da imagem de saída
    @param model: modelo rembg (u2net, u2net_human_seg, etc.)
    @param alpha_matting: ativar alpha matting para bordas suaves
    @param ae: erosão do alpha matting
    @param ab: blur do alpha matting
    """
    cmd = [str(REMBG_BIN), "i"]

    if model:
        cmd.extend(["-m", model])
    if alpha_matting:
        cmd.extend(["-a", "-ae", str(ae), "-ab", str(ab)])

    cmd.extend([input_path, output_path])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {output_path}")


def process_batch(input_dir: str, output_dir: str | None = None, **kwargs) -> None:
    """Processa todas as imagens de uma pasta.

    @param input_dir: pasta com imagens de entrada
    @param output_dir: pasta para salvar resultados (None = in-place)
    """
    input_path = Path(input_dir)
    in_place = output_dir is None or Path(output_dir) == input_path

    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
    images = [f for f in input_path.iterdir()
              if f.suffix.lower() in extensions and SUFFIX not in f.stem]

    if not images:
        print(f"Nenhuma imagem encontrada em '{input_dir}'", file=sys.stderr)
        sys.exit(1)

    if not in_place:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"Processando {len(images)} imagens...")
    for img_file in sorted(images):
        if in_place:
            out_file = resolve_output_path(str(img_file))
            run_rembg(str(img_file.parent / f"{img_file.stem}{SUFFIX}{img_file.suffix}"),
                      out_file, **kwargs)
        else:
            out_file = str(Path(output_dir) / f"{img_file.stem}.png")
            run_rembg(str(img_file), out_file, **kwargs)

    dest = input_dir if in_place else output_dir
    print(f"Concluído: {len(images)} imagens processadas em '{dest}'")


def main():
    parser = argparse.ArgumentParser(
        description="Remove background de imagens usando rembg"
    )
    parser.add_argument("input", help="Imagem ou pasta de entrada")
    parser.add_argument("output", nargs="?", default=None,
                        help="Imagem ou pasta de saída (opcional: sem informar, "
                             "renomeia original para _original e salva limpa no nome original)")
    parser.add_argument(
        "-m", "--model", default=None,
        help="Modelo rembg: u2net (padrão), u2net_human_seg, isnet-general-use, silueta"
    )
    parser.add_argument(
        "-a", "--alpha-matting", action="store_true",
        help="Ativar alpha matting (bordas mais suaves)"
    )
    parser.add_argument(
        "-ae", type=int, default=10,
        help="Erosão do alpha matting (padrão: 10)"
    )
    parser.add_argument(
        "-ab", type=int, default=10,
        help="Blur do alpha matting (padrão: 10)"
    )

    args = parser.parse_args()
    input_path = Path(args.input)

    if not REMBG_BIN.exists():
        print(f"Erro: rembg não encontrado em {REMBG_BIN}", file=sys.stderr)
        print("Execute o script de setup primeiro.", file=sys.stderr)
        sys.exit(1)

    kwargs = dict(
        model=args.model,
        alpha_matting=args.alpha_matting,
        ae=args.ae,
        ab=args.ab,
    )

    if input_path.is_dir():
        process_batch(args.input, args.output, **kwargs)
    else:
        if args.output:
            output = args.output
        else:
            output = resolve_output_path(args.input)
            # Atualizar input para ler do arquivo renomeado
            args.input = str(input_path.parent / f"{input_path.stem}{SUFFIX}{input_path.suffix}")

        run_rembg(args.input, output, **kwargs)


if __name__ == "__main__":
    main()
