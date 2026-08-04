#!/usr/bin/env python3
"""Cierra una sesión: calcula el `resultado` desde respuestas.jsonl y lo escribe en sesiones.jsonl.

    python3 cerrar_sesion.py --sesion 2026-08-04-1232

El recuento no se estima: sale de las respuestas registradas. Si la sesión no tiene
respuestas, no se escribe nada — una sesión a medias se queda a medias.
"""

import argparse
import json
from collections import defaultdict

from comun import RESPUESTAS, SESIONES, leer_jsonl, reescribir_linea, verificar_datos


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sesion", required=True)
    args = p.parse_args()

    verificar_datos()
    sesiones = leer_jsonl(SESIONES)
    fila = next((s for s in sesiones if s.get("id") == args.sesion), None)
    if fila is None:
        raise SystemExit(f"la sesión {args.sesion!r} no está en sesiones.jsonl")

    respuestas = [r for r in leer_jsonl(RESPUESTAS)
                  if r.get("sesion") == args.sesion and not r.get("repaso")]
    if not respuestas:
        raise SystemExit(
            f"la sesión {args.sesion!r} no tiene respuestas registradas — se queda sin resultado"
        )

    fallos = defaultdict(int)
    for r in respuestas:
        if not r.get("correcto"):
            fallos[r.get("subtema_id") or r.get("tema_id")] += 1

    aciertos = sum(1 for r in respuestas if r.get("correcto"))
    fila["resultado"] = {
        "ejercicios": len(respuestas),
        "aciertos": aciertos,
        "parciales": sum(1 for r in respuestas if r.get("parcial")),
        "tasa": round(aciertos / len(respuestas), 3),
        "temas_flojos": [t for t, _ in sorted(fallos.items(), key=lambda kv: -kv[1]) if t],
    }
    reescribir_linea(SESIONES, "id", args.sesion, fila)
    print(json.dumps(fila, ensure_ascii=False))


if __name__ == "__main__":
    main()
