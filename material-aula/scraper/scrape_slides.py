#!/usr/bin/env python3
"""
Scraper de slides PDF — extrai texto e imagens de todos os PDFs na pasta.

Saída por PDF:
  output/<nome_pdf>/
    content.md          — texto completo, página por página
    images_index.json   — índice de imagens do PDF
    images/             — imagens extraídas

Saída combinada:
  output/
    all_content.md      — markdown unificado de todos os PDFs
    images_index.json   — índice unificado
    images/             — todas as imagens (prefixadas pelo nome do PDF)

Flags:
  --describe            Usa a API do Gemini para descrever cada imagem
  --api-key KEY         Chave da API Gemini (ou defina GEMINI_API_KEY no ambiente)
"""

import sys
import json
import re
import time
import argparse
import os
from pathlib import Path
import pymupdf  # PyMuPDF


OUTPUT_DIR = Path("output")


# ── Gemini ─────────────────────────────────────────────────────────────────────

def build_gemini_describer(api_key: str):
    """Retorna uma função que descreve uma imagem via Gemini (SDK google-genai, API v1)."""
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        print("Instalando google-genai ...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-genai"])
        from google import genai
        from google.genai import types as genai_types

    client = genai.Client(api_key=api_key)

    PROMPT = (
        "Esta é uma imagem de um slide de aula de Engenharia de Software. "
        "Descreva de forma objetiva e técnica o que está representado: "
        "diagramas, código, texto principal, tipo de conteúdo (diagrama UML, "
        "fluxograma, tabela, código-fonte, etc.). Seja conciso (2-4 frases)."
    )

    MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif", "webp": "image/webp"}

    def describe(img_path: Path) -> str:
        mime = MIME.get(img_path.suffix.lstrip(".").lower(), "image/png")
        max_retries = 5
        for attempt in range(max_retries):
            try:
                img_bytes = img_path.read_bytes()
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[
                        genai_types.Part.from_text(text=PROMPT),
                        genai_types.Part.from_bytes(data=img_bytes, mime_type=mime),
                    ],
                )
                return response.text.strip()
            except Exception as e:
                msg = str(e)
                match = re.search(r"retry_delay\s*\{\s*seconds:\s*(\d+)", msg)
                wait = int(match.group(1)) + 2 if match else 2 ** (attempt + 2)
                if attempt < max_retries - 1 and ("429" in msg or "quota" in msg.lower()):
                    print(f"\n    [rate limit] aguardando {wait}s ...", end=" ", flush=True)
                    time.sleep(wait)
                else:
                    return f"[erro ao descrever: {e}]"
        return "[erro: máximo de tentativas atingido]"

    return describe


# ── Helpers ────────────────────────────────────────────────────────────────────

def sanitize(text: str) -> str:
    return re.sub(r"[^\S\n]+", " ", text).strip()


def extract_page_title(text: str, page_num: int) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            slug = re.sub(r"[^a-zA-Z0-9À-ú ]", "", line)[:60].strip()
            slug = re.sub(r"\s+", "_", slug)
            return slug or f"pagina_{page_num}"
    return f"pagina_{page_num}"


# ── Processamento por PDF ──────────────────────────────────────────────────────

def process_pdf(pdf_path: Path, describer=None):
    pdf_name = pdf_path.stem
    out_dir = OUTPUT_DIR / pdf_name
    img_dir = out_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(str(pdf_path))
    total_pages = doc.page_count

    md_lines = [
        f"# {pdf_name}",
        f"_Total de páginas: {total_pages}_\n",
    ]

    image_index: list[dict] = []
    total_images = 0

    for page_num, page in enumerate(doc, start=1):
        raw_text = page.get_text("text")
        text = sanitize(raw_text)
        title_slug = extract_page_title(text, page_num)

        md_lines.append(f"## Página {page_num} — {title_slug.replace('_', ' ')}")
        md_lines.append("")
        if text:
            md_lines.append(text)
        else:
            md_lines.append("_(sem texto extraível nesta página)_")
        md_lines.append("")

        img_list = page.get_images(full=True)
        for img_idx, img_info in enumerate(img_list, start=1):
            xref = img_info[0]
            try:
                base_img = doc.extract_image(xref)
            except Exception as e:
                print(f"  [aviso] não foi possível extrair imagem xref={xref}: {e}")
                continue

            ext = base_img["ext"]
            img_bytes = base_img["image"]

            filename = f"p{page_num:03d}_img{img_idx:02d}__{title_slug}.{ext}"
            img_path = img_dir / filename
            img_path.write_bytes(img_bytes)

            entry: dict = {
                "arquivo": str(img_path.relative_to(OUTPUT_DIR)),
                "pdf": pdf_name,
                "pagina": page_num,
                "titulo_pagina": title_slug.replace("_", " "),
                "indice_na_pagina": img_idx,
                "formato": ext,
            }

            if describer:
                print(f"    descrevendo {filename} ...", end=" ", flush=True)
                entry["descricao"] = describer(img_path)
                print("ok")
                time.sleep(4)  # 15 RPM = 1 req/4s no tier gratuito

            total_images += 1
            image_index.append(entry)

            md_lines.append(f"![p{page_num}_img{img_idx}](images/{filename})")
            md_lines.append("")

    doc.close()

    (out_dir / "content.md").write_text("\n".join(md_lines), encoding="utf-8")

    if image_index:
        (out_dir / "images_index.json").write_text(
            json.dumps(image_index, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    return total_pages, total_images, md_lines, image_index


# ── Saída combinada ────────────────────────────────────────────────────────────

def generate_combined(all_md_lines: list[list[str]], all_image_indexes: list[list[dict]]):
    combined_img_dir = OUTPUT_DIR / "images"
    combined_img_dir.mkdir(exist_ok=True)

    combined_md: list[str] = ["# Todos os Slides\n"]
    combined_index: list[dict] = []

    for md_lines, img_entries in zip(all_md_lines, all_image_indexes):
        seen: set[str] = set()
        entries_by_file: dict[str, dict] = {}
        for entry in img_entries:
            src_path = OUTPUT_DIR / entry["arquivo"]
            if str(src_path) not in seen:
                seen.add(str(src_path))
                entries_by_file[str(src_path)] = entry

        rename_map: dict[str, str] = {}
        for src_str, entry in entries_by_file.items():
            src_path = Path(src_str)
            new_filename = f"{entry['pdf']}_{src_path.name}"
            dst_path = combined_img_dir / new_filename
            dst_path.write_bytes(src_path.read_bytes())
            rename_map[entry["arquivo"]] = new_filename
            combined_index.append({**entry, "arquivo": f"images/{new_filename}"})

        for line in md_lines:
            if line.startswith("![") and "](images/" in line:
                old_name = line.split("](images/")[1].rstrip(")")
                new_name = next(
                    (v for k, v in rename_map.items() if k.endswith(old_name)),
                    old_name,
                )
                combined_md.append(f"{line.split('](images/')[0]}](images/{new_name})")
            else:
                combined_md.append(line)
        combined_md.append("\n---\n")

    (OUTPUT_DIR / "all_content.md").write_text("\n".join(combined_md), encoding="utf-8")
    (OUTPUT_DIR / "images_index.json").write_text(
        json.dumps(combined_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Scraper de slides PDF")
    parser.add_argument(
        "--describe", action="store_true",
        help="Usa Gemini para descrever cada imagem extraída"
    )
    parser.add_argument(
        "--api-key", default=os.environ.get("GEMINI_API_KEY", ""),
        help="Chave da API Gemini (padrão: variável GEMINI_API_KEY)"
    )
    args = parser.parse_args()

    describer = None
    if args.describe:
        if not args.api_key:
            print("Erro: --describe requer --api-key ou a variável GEMINI_API_KEY.")
            sys.exit(1)
        describer = build_gemini_describer(args.api_key)
        print("Descrição de imagens via Gemini ativada.\n")

    script_dir = Path(__file__).parent
    pdfs = sorted(script_dir.glob("*.pdf"))

    if not pdfs:
        print("Nenhum arquivo .pdf encontrado na pasta.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Encontrados {len(pdfs)} PDFs.\n")
    grand_pages = grand_images = 0
    all_md_lines: list[list[str]] = []
    all_image_indexes: list[list[dict]] = []

    for pdf_path in pdfs:
        print(f"Processando: {pdf_path.name} ...", end=" ", flush=True)
        pages, images, md_lines, image_index = process_pdf(pdf_path, describer)
        grand_pages += pages
        grand_images += images
        all_md_lines.append(md_lines)
        all_image_indexes.append(image_index)
        print(f"{pages} páginas, {images} imagens.")

    print("\nGerando saída combinada ...", end=" ", flush=True)
    generate_combined(all_md_lines, all_image_indexes)
    print("pronto.")

    print(f"\nConcluído! Total: {grand_pages} páginas, {grand_images} imagens.")
    print(f"Saída por PDF em: {(script_dir / OUTPUT_DIR).resolve()}")
    print(f"Saída combinada:  {(script_dir / OUTPUT_DIR).resolve()}/all_content.md")


if __name__ == "__main__":
    main()
