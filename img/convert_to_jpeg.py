#!/usr/bin/env python3
"""
Script para converter todas as imagens de um diretório para formato JPEG.

Uso:
    python convert_to_jpeg.py

O script busca todos os arquivos de imagem no diretório atual que não sejam JPEG
e os converte para JPEG, mantendo o nome original e substituindo a extensão.
"""

import os
from pathlib import Path
from PIL import Image

# Formatos de imagem suportados (excluindo JPEG/JPG)
SUPPORTED_FORMATS = {".png", ".bmp", ".gif", ".tiff", ".tif", ".webp", ".ico"}


def convert_to_jpeg(image_path: Path) -> bool:
    """
    Converte uma imagem para formato JPEG.

    Args:
        image_path: Caminho para o arquivo de imagem

    Returns:
        True se a conversão foi bem-sucedida, False caso contrário
    """
    try:
        # Abre a imagem
        img = Image.open(image_path)

        # Converte para RGB se necessário (JPEG não suporta transparência)
        if img.mode in ("RGBA", "LA", "P"):
            # Cria um fundo branco
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Define o caminho de saída (mesmo nome, extensão .jpg)
        output_path = image_path.with_suffix(".jpg")

        # Salva a imagem em JPEG com qualidade alta
        img.save(output_path, "JPEG", quality=95, optimize=True)

        print(f"✅ Convertido: {image_path.name} → {output_path.name}")

        # Remove o arquivo original após conversão bem-sucedida
        image_path.unlink()
        print(f"🗑️  Removido arquivo original: {image_path.name}")

        return True

    except Exception as e:
        print(f"❌ Erro ao converter {image_path.name}: {str(e)}")
        return False


def main():
    """Função principal que busca e converte imagens."""
    # Diretório atual onde o script está sendo executado
    current_dir = Path.cwd()

    print(f"📁 Buscando imagens em: {current_dir}")
    print(f"🔍 Formatos suportados: {', '.join(SUPPORTED_FORMATS)}")
    print("-" * 60)

    # Busca todos os arquivos no diretório atual
    image_files = [
        f
        for f in current_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS
    ]

    if not image_files:
        print("ℹ️  Nenhuma imagem encontrada para conversão.")
        return

    print(f"📊 Encontradas {len(image_files)} imagem(ns) para converter\n")

    # Converte cada imagem
    success_count = 0
    for image_file in image_files:
        if convert_to_jpeg(image_file):
            success_count += 1
        print()  # Linha em branco para separar

    # Resumo da operação
    print("-" * 60)
    print(
        f"✨ Conversão concluída: {success_count}/{len(image_files)} imagens convertidas com sucesso"
    )


if __name__ == "__main__":
    main()
