#!/usr/bin/env python3
"""Consulta el catálogo oficial de temas (references/temas.json, derivado del PCIC).

    python3 temas.py --listar                 # todos, con id y nombre
    python3 temas.py --listar --bloque FR     # solo la zona fronteriza B1→B2
    python3 temas.py --buscar subjuntivo      # id por texto libre
    python3 temas.py --id G.B2.condicionales-irreales --json

Sirve para traducir «lo que dice el usuario» a un id antes de registrar nada.
"""

import argparse
import json

from comun import catalogo


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--listar", action="store_true")
    p.add_argument("--buscar")
    p.add_argument("--id")
    p.add_argument("--bloque", choices=["G", "F", "LX", "FR"])
    p.add_argument("--nivel", choices=["B1", "B2", "B1/B2"])
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    temas = list(catalogo().values())
    if args.bloque:
        temas = [t for t in temas if t["bloque"] == args.bloque]
    if args.nivel:
        temas = [t for t in temas if t["nivel"] == args.nivel]
    if args.id:
        temas = [t for t in temas if t["id"] == args.id]
    if args.buscar:
        q = args.buscar.lower()
        temas = [t for t in temas
                 if q in t["id"].lower() or q in t["nombre"].lower()
                 or q in t.get("motivo", "").lower()]

    if args.json:
        print(json.dumps(temas, ensure_ascii=False, indent=2))
        return
    if not temas:
        raise SystemExit("ningún tema coincide")
    for t in temas:
        frontera = f"  → {t['frontera']}" if t.get("frontera") else ""
        print(f"{t['id']:<45} {t['nivel']:<6} {t['amplitud']:<8} {t['nombre']}{frontera}")


if __name__ == "__main__":
    main()
