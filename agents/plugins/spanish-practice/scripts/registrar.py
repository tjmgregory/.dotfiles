#!/usr/bin/env python3
"""Registra una respuesta del usuario en respuestas.jsonl. Una llamada por ejercicio corregido.

    python3 registrar.py --sesion 2026-08-04-1232 --n 3/8 \
        --tema-id G.B1.pronombres-atonos --subtema-id FR.valores-de-se \
        --formato completar --correcto no \
        --respuesta "se me olvidó las llaves" --esperada "se me olvidaron las llaves" \
        --tipo error --nota "concordancia con el sujeto pospuesto"

Se llama **en el mismo turno en que se corrige el ejercicio**, no al final de la sesión:
si el usuario se va a medias, lo respondido hasta ahí queda guardado igual.

Tema y subtema van siempre por id del catálogo oficial (references/temas.json). El
subtema es el punto estrecho que mide de verdad el ejercicio, y es lo que luego
decide en qué se insiste.
"""

import argparse
import json
from datetime import datetime

from comun import (RESPUESTAS, SESIONES, anadir_jsonl, config, exigir_tema,
                   leer_jsonl, verificar_datos)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sesion", required=True, help="id devuelto por abrir_sesion.py")
    p.add_argument("--n", required=True, help="posición del ejercicio, p. ej. 3/8")
    p.add_argument("--tema-id", required=True, help="id del catálogo — resuélvelo con temas.py")
    p.add_argument("--subtema-id", default=None,
                   help="id del catálogo, más estrecho que el tema; normalmente un FR.*")
    p.add_argument("--formato", required=True,
                   choices=["opciones", "texto-libre", "completar", "identificar-error"])
    p.add_argument("--correcto", required=True, choices=["si", "no", "parcial"])
    p.add_argument("--respuesta", required=True, help="lo que puso el usuario, literal")
    p.add_argument("--esperada", required=True)
    p.add_argument("--tipo", default=None, choices=["error", "preferencia"],
                   help="solo si no fue correcto: agramatical vs. poco idiomático")
    p.add_argument("--nota", default=None, help="la regla que falló, en una línea")
    p.add_argument("--nivel", default=None)
    p.add_argument("--repaso", action="store_true",
                   help="marca el ítem como parte del repaso de apertura, no del tema del día")
    args = p.parse_args()

    verificar_datos()
    if args.sesion not in {s.get("id") for s in leer_jsonl(SESIONES)}:
        raise SystemExit(
            f"la sesión {args.sesion!r} no está en sesiones.jsonl — ábrela con abrir_sesion.py"
        )

    tema = exigir_tema(args.tema_id)
    subtema = exigir_tema(args.subtema_id) if args.subtema_id else None

    fila = {
        "sesion": args.sesion,
        "ts": datetime.now().isoformat(timespec="seconds"),
        "n": args.n,
        "tema_id": tema["id"],
        "tema": tema["nombre"],
        "subtema_id": subtema["id"] if subtema else None,
        "subtema": subtema["nombre"] if subtema else None,
        "formato": args.formato,
        "nivel": args.nivel or config()["nivel"],
        "correcto": args.correcto == "si",
        "parcial": args.correcto == "parcial",
        "respuesta": args.respuesta,
        "esperada": args.esperada,
        "tipo": args.tipo,
        "nota": args.nota,
        "repaso": args.repaso,
    }
    anadir_jsonl(RESPUESTAS, fila)
    print(json.dumps(fila, ensure_ascii=False))


if __name__ == "__main__":
    main()
