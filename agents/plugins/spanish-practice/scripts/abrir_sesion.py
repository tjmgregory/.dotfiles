#!/usr/bin/env python3
"""Abre una sesión: genera el id con el reloj del sistema y lo añade a sesiones.jsonl.

    python3 abrir_sesion.py --tema-id FR.valores-de-se --formato completar --ritmo uno-a-uno

Imprime el id de la sesión en stdout: es el que hay que pasar a registrar.py.
El tema se identifica siempre por su id del catálogo oficial (references/temas.json);
el nivel sale de config.json. Ninguno de los dos se escribe a mano.
"""

import argparse
import json
from datetime import datetime

from comun import (SESIONES, anadir_jsonl, config, exigir_tema, leer_jsonl,
                   verificar_datos)


def id_libre(ahora, usados):
    """Minuto a minuto, pero sin colisiones: dos sesiones en el mismo minuto fundirían sus datos."""
    base = ahora.strftime("%Y-%m-%d-%H%M")
    if base not in usados:
        return base
    for sufijo in "bcdefghijklmnopqrstuvwxyz":
        if f"{base}{sufijo}" not in usados:
            return f"{base}{sufijo}"
    raise SystemExit(f"demasiadas sesiones en el minuto {base}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tema-id", help="id del catálogo — resuélvelo con temas.py; no aplica en repaso")
    p.add_argument("--formato",
                   choices=["opciones", "texto-libre", "completar", "identificar-error"])
    p.add_argument("--ritmo", choices=["uno-a-uno", "tanda"])
    p.add_argument("--tipo", default="practica", choices=["practica", "repaso"])
    p.add_argument("--repaso-apertura", default="no", choices=["si", "no"])
    p.add_argument("--nivel", help="solo para saltarse el perfil en un caso puntual")
    args = p.parse_args()

    verificar_datos()
    if args.tipo == "practica" and not (args.tema_id and args.formato):
        raise SystemExit("una sesión de práctica necesita --tema-id y --formato")
    tema = exigir_tema(args.tema_id) if args.tema_id else None
    cfg = config()
    ahora = datetime.now()
    fila = {
        "id": id_libre(ahora, {s.get("id") for s in leer_jsonl(SESIONES)}),
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M"),
        "tipo": args.tipo,
        "tema_id": tema["id"] if tema else None,
        "tema": tema["nombre"] if tema else None,
        "nivel_tema": tema["nivel"] if tema else None,
        "formato": args.formato,
        "nivel": args.nivel or cfg["nivel"],
        "ritmo": args.ritmo or cfg["ritmo_por_defecto"],
        "repaso_apertura": args.repaso_apertura == "si",
    }
    anadir_jsonl(SESIONES, fila)
    print(fila["id"])
    print(json.dumps(fila, ensure_ascii=False))


if __name__ == "__main__":
    main()
