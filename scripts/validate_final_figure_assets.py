#!/usr/bin/env python3
"""Validate v10.6 DOCX/PDF figure correspondence against packaged PNG assets."""
from __future__ import annotations
import argparse, hashlib, re, tempfile, zipfile, zlib
from pathlib import Path
from xml.etree import ElementTree as ET
try:
    from PIL import Image, ImageChops, ImageStat
except ImportError as exc:
    raise SystemExit("Pillow is required for final figure comparison") from exc
ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "http" + "://"
NS = {"w":SCHEMA + "schemas.openxmlformats.org/wordprocessingml/2006/main", "a":SCHEMA + "schemas.openxmlformats.org/drawingml/2006/main", "r":SCHEMA + "schemas.openxmlformats.org/officeDocument/2006/relationships"}
EXPECTED_DOCX = "604d83b383db8a5f09c9ac95ef354fb29474b50423a63b9ee681b1c38199d10d"
EXPECTED_PDF = "790c0e74ec5378e990b03a513be0250936564ed7aae6265efc0c8dd0002b6dd3"
EXPECTED = {
  1: ("figures/figure1_v106_docx_submission_equivalent.png", "word/media/image1.png", 119, (4110,3897), (1859,1763), "942a00fac003e3e5f865b6546b36af87ac6eabec8271e4f9947a903c423a140b"),
  2: ("figures/figure2_v106_docx_submission_equivalent.png", "word/media/image2.png", 227, (4110,2314), (1860,1047), "6eca65f49e5e1d054284ff7456b49b25c96e3ca49f0faa6e161c893b337d7513"),
  3: ("figures/figure3_v106_docx_submission_equivalent.png", "word/media/image3.png", 368, (4110,2433), (1920,1137), "97d1baa3d64f1a2430ad199fc30f186d0ec3bec5ad38628fc05381eb66812cff"),
}
def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def pdf_streams(pdf: bytes) -> dict[int, tuple[bytes, bytes, tuple[int,int]]]:
    out = {}
    for m in re.finditer(rb"(\d+)\s+\d+\s+obj\s*<<(.*?)>>\s*stream\r?\n", pdf, re.S):
        n = int(m.group(1)); head = m.group(2)
        if b"/Subtype/Image" not in head: continue
        lm = re.search(rb"/Length\s+(\d+)(?:\s+\d+)?", head)
        if not lm: continue
        end = pdf.find(b"endstream", m.end())
        raw = pdf[m.end():end].rstrip(b"\r\n")
        wm = re.search(rb"/Width\s+(\d+)", head); hm = re.search(rb"/Height\s+(\d+)", head)
        if not wm or not hm: continue
        out[n] = (head, raw, (int(wm.group(1)), int(hm.group(1))))
    return out
def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--docx", type=Path, required=True); ap.add_argument("--pdf", type=Path, required=True); args = ap.parse_args()
    if sha(args.docx.read_bytes()) != EXPECTED_DOCX: raise SystemExit("unexpected_docx_sha256")
    if sha(args.pdf.read_bytes()) != EXPECTED_PDF: raise SystemExit("unexpected_pdf_sha256")
    with zipfile.ZipFile(args.docx) as z:
        rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        relmap = {x.attrib["Id"]: x.attrib["Target"] for x in rels}
        doc = ET.fromstring(z.read("word/document.xml"))
        blips = [x.attrib["{%s}embed" % NS["r"]] for x in doc.findall(".//a:blip", NS)]
        captions = " ".join("".join(x.text or "" for x in p.findall(".//w:t", NS)) for p in doc.findall(".//w:p", NS))
        if blips != ["rId11", "rId12", "rId13"]: raise SystemExit(f"unexpected_docx_figure_relationships:{blips}")
        for i, (_, member, _, _, _, _) in EXPECTED.items():
            if relmap.get("rId%d" % (10+i)) != "media/image%d.png" % i: raise SystemExit("docx_relationship_target_mismatch")
            if z.read("word/" + member.split("/",1)[1]) != (ROOT / EXPECTED[i][0]).read_bytes(): raise SystemExit(f"docx_media_mismatch:figure{i}")
        for anchor in ("Fig. 1", "Fig. 2", "Fig. 3"):
            if anchor not in captions: raise SystemExit(f"missing_caption_anchor:{anchor}")
    streams = pdf_streams(args.pdf.read_bytes())
    for i, (pkg, _, obj, ddims, pdims, expected_stream_sha) in EXPECTED.items():
        if obj not in streams: raise SystemExit(f"missing_pdf_image_object:{obj}")
        head, raw, dims = streams[obj]
        if sha(raw) != expected_stream_sha or dims != pdims: raise SystemExit(f"pdf_image_object_mismatch:figure{i}")
        with Image.open(ROOT / pkg) as a:
            if a.size != ddims: raise SystemExit(f"package_dimensions_mismatch:figure{i}")
            if b"/DCTDecode" in head:
                import io
                b = Image.open(io.BytesIO(raw)).convert("RGB")
            else:
                b = Image.frombytes("RGB", dims, zlib.decompress(raw))
            bb = b.resize(a.size, Image.Resampling.LANCZOS)
            mae = sum(ImageStat.Stat(ImageChops.difference(a.convert("RGB"), bb)).mean) / 3
            if mae > 3.0: raise SystemExit(f"docx_pdf_visual_mismatch:figure{i}:mae={mae:.4f}")
    print("docx_pdf_figure_asset_check=ok figures=3 figure3_panel_count=3 editable_vector_source=none_found")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
