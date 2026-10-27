"""
pdf_para_jpeg.py
----------------
Converte todos os PDFs de uma pasta em imagens JPEG.
Para cada PDF, cria uma subpasta e salva cada página como página_001.jpg, página_002.jpg, etc.

Uso:
    python pdf_para_jpeg.py <pasta_com_pdfs>

    Exemplo:
    python pdf_para_jpeg.py "C:/Users/Voce/Documents/meus_pdfs"
    python pdf_para_jpeg.py "/home/voce/meus_pdfs"

Requisitos:
    pip install pdf2image pillow
    + Poppler (veja instruções abaixo)
"""

import sys
import os
from pathlib import Path

# ──────────────────────────────────────────────
#  CONFIGURAÇÕES — ajuste aqui se quiser
# ──────────────────────────────────────────────
DPI = 200          # Resolução das imagens (150 = rápido/menor, 300 = alta qualidade)
QUALIDADE_JPEG = 90  # Qualidade JPEG (1-95). 85-95 é ótimo equilíbrio
# ──────────────────────────────────────────────


def converter_pdf(pdf_path: Path, pasta_saida: Path, dpi: int, qualidade: int):
    from pdf2image import convert_from_path

    nome_pdf = pdf_path.stem  # nome sem extensão
    pasta_pdf = pasta_saida / nome_pdf
    pasta_pdf.mkdir(parents=True, exist_ok=True)

    print(f"\n📄 Processando: {pdf_path.name}")
    print(f"   📁 Pasta de saída: {pasta_pdf}")

    paginas = convert_from_path(str(pdf_path), dpi=dpi)
    total = len(paginas)

    for i, pagina in enumerate(paginas, start=1):
        nome_arquivo = f"pagina_{i:03d}.jpg"
        caminho_arquivo = pasta_pdf / nome_arquivo
        pagina.save(str(caminho_arquivo), "JPEG", quality=qualidade)
        print(f"   ✅ {nome_arquivo}  ({i}/{total})", end="\r")

    print(f"   ✅ {total} páginas salvas em: {pasta_pdf}          ")
    return total


def main():
    # ── Pasta de entrada ──────────────────────
    if len(sys.argv) > 1:
        pasta_entrada = Path(sys.argv[1])
    else:
        # Se não passar argumento, pede interativamente
        caminho = input("📂 Cole o caminho da pasta com os PDFs: ").strip().strip('"')
        pasta_entrada = Path(caminho)

    if not pasta_entrada.exists():
        print(f"❌ Pasta não encontrada: {pasta_entrada}")
        sys.exit(1)

    # ── Pasta de saída (subpasta "jpgs" dentro da mesma pasta) ───
    pasta_saida = pasta_entrada / "jpgs"
    pasta_saida.mkdir(exist_ok=True)

    # ── Busca PDFs ────────────────────────────
    pdfs = sorted(pasta_entrada.glob("*.pdf"))
    if not pdfs:
        pdfs = sorted(pasta_entrada.glob("*.PDF"))  # maiúsculas no Windows

    if not pdfs:
        print("❌ Nenhum arquivo .pdf encontrado na pasta.")
        sys.exit(1)

    print(f"\n🔍 {len(pdfs)} PDF(s) encontrado(s) em: {pasta_entrada}")
    print(f"📁 Imagens serão salvas em: {pasta_saida}")
    print(f"⚙️  DPI: {DPI} | Qualidade JPEG: {QUALIDADE_JPEG}")
    print("─" * 50)

    total_paginas = 0
    erros = []

    for pdf in pdfs:
        try:
            total_paginas += converter_pdf(pdf, pasta_saida, DPI, QUALIDADE_JPEG)
        except Exception as e:
            print(f"\n⚠️  Erro em {pdf.name}: {e}")
            erros.append(pdf.name)

    # ── Resumo ────────────────────────────────
    print("\n" + "═" * 50)
    print(f"✅ Concluído! {len(pdfs) - len(erros)}/{len(pdfs)} PDFs processados")
    print(f"🖼️  Total de páginas exportadas: {total_paginas}")
    if erros:
        print(f"⚠️  Arquivos com erro: {', '.join(erros)}")
    print(f"📁 Resultado em: {pasta_saida.resolve()}")


if __name__ == "__main__":
    main()
