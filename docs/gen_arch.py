"""Regenerates docs/architecture.drawio (run from repo root)."""

NODES = [
    ("dev", "Developer / CLI", 20, 200, 140, 60, "#dae8fc"),
    (
        "api",
        "Copilot API (FastAPI)\nCPU pool, ns api-copilot",
        240,
        200,
        190,
        70,
        "#d5e8d4",
    ),
    (
        "emb",
        "Embedding pod\nHF TEI cpu-1.9\nbge-base-en-v1.5 (768d)",
        560,
        40,
        200,
        70,
        "#d5e8d4",
    ),
    (
        "sql",
        "Cloud SQL Postgres 16 + pgvector\n(PSC, Auth Proxy, IAM auth)",
        560,
        200,
        200,
        70,
        "#ffe6cc",
    ),
    (
        "llm",
        "vLLM on GPU pool (Spot L4, tainted, 0-1)\nQwen2.5-7B-Instruct FP16",
        540,
        360,
        240,
        80,
        "#f8cecc",
    ),
    (
        "ing",
        "Ingest Job\nOpenAPI -> chunk per op -> embed",
        240,
        40,
        190,
        60,
        "#d5e8d4",
    ),
    ("gcs", "GCS bucket (kept)\nmodel weights cache", 860, 360, 150, 60, "#fff2cc"),
    ("otel", "OpenLIT (ns openlit)\nOTLP 4317/4318", 240, 380, 190, 60, "#e1d5e7"),
]
# id, src, dst, label, exit(x,y), entry(x,y), waypoints
EDGES = [
    ("e0", "dev", "api", "HTTPS /v1/ask", (1, 0.5), (0, 0.5), []),
    ("e1", "api", "emb", "embed query", (1, 0.15), (0, 0.8), [(530, 210), (530, 96)]),
    ("e2", "api", "sql", "vector search", (1, 0.5), (0, 0.5), []),
    (
        "e3",
        "api",
        "llm",
        "chat completions",
        (1, 0.85),
        (0, 0.3),
        [(500, 260), (500, 384)],
    ),
    ("e4", "ing", "emb", "embed docs", (1, 0.3), (0, 0.2), [(500, 58), (500, 54)]),
    (
        "e5",
        "ing",
        "sql",
        "upsert chunks",
        (1, 0.8),
        (0.2, 0),
        [(450, 88), (450, 160), (610, 160)],
    ),
    ("e6", "llm", "gcs", "load weights", (1, 0.5), (0, 0.5), []),
    ("e7", "api", "otel", "OTLP (all services)", (0.5, 1), (0.5, 0), []),
]


def esc(s):
    return s.replace("\n", "&#10;")


HEADER = (
    '<mxfile><diagram name="architecture"><mxGraphModel dx="1000" dy="600" grid="1" pageWidth="1100" pageHeight="520">'
    '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
)
out = [HEADER]
for i, t, x, y, w, h, c in NODES:
    out.append(
        f'<mxCell id="{i}" value="{esc(t)}" style="rounded=1;whiteSpace=wrap;html=0;'
        f'fillColor={c};strokeColor=#333333;fontSize=11;" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
    )
for i, s, t, lab, ex, en, pts in EDGES:
    wp = ""
    if pts:
        wp = (
            '<Array as="points">'
            + "".join(f'<mxPoint x="{a}" y="{b}"/>' for a, b in pts)
            + "</Array>"
        )
    out.append(
        f'<mxCell id="{i}" value="{esc(lab)}" style="endArrow=block;html=1;fontSize=10;'
        f"labelBackgroundColor=#ffffff;exitX={ex[0]};exitY={ex[1]};entryX={en[0]};entryY={en[1]};"
        f'edgeStyle=orthogonalEdgeStyle;" edge="1" source="{s}" target="{t}" parent="1">'
        f'<mxGeometry relative="1" as="geometry">{wp}</mxGeometry></mxCell>'
    )
out.append(
    '<mxCell id="note" value="Cloud SQL and the GPU pool are deleted by down.sh at teardown; '
    'check-no-billable.sh verifies." style="text;fontSize=11;" vertex="1" parent="1">'
    '<mxGeometry x="20" y="480" width="700" height="20" as="geometry"/></mxCell>'
)
out.append("</root></mxGraphModel></diagram></mxfile>")
with open("docs/architecture.drawio", "w") as f:
    f.write("\n".join(out))
