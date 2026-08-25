#!/usr/bin/env python3
"""Tasas de acierto sobre todo el histórico + sugerencia de apertura.

    python3 estadisticas.py            # informe legible
    python3 estadisticas.py --json     # el mismo cálculo, en JSON
    python3 estadisticas.py --tema-id FR.valores-de-se   # el detalle de un tema

Aquí no hay criterio del modelo: todo sale de respuestas.jsonl, del catálogo oficial
de temas y de los umbrales de config.json. La regla es insistir en el mismo tema
hasta consolidarlo y solo entonces rotar.
"""

import argparse
import json
from collections import defaultdict

from comun import (DATA, RESPUESTAS, SESIONES, catalogo, config, leer_jsonl,
                   verificar_datos)

FORMATOS_ROTACION = ["completar", "opciones", "texto-libre"]


def puntos(fila):
    """Un acierto vale 1, un parcial 0,5, un fallo 0."""
    if fila.get("correcto"):
        return 1.0
    return 0.5 if fila.get("parcial") else 0.0


def tasa(filas):
    return sum(puntos(f) for f in filas) / len(filas) if filas else None


def resumen(filas, temas):
    t = tasa(filas)
    return {
        "n": len(filas),
        "aciertos": sum(1 for f in filas if f.get("correcto")),
        "parciales": sum(1 for f in filas if f.get("parcial")),
        "tasa": round(t, 3) if t is not None else None,
    }


def normalizar_tema(fila, temas):
    """El id del catálogo. Las filas antiguas sin id se resuelven por nombre."""
    tid = fila.get("tema_id")
    if tid in temas:
        return tid
    nombre = (fila.get("tema") or "").strip().lower()
    if not nombre:
        return None
    exacto = next((t for t in temas.values() if nombre == t["nombre"].lower()), None)
    if exacto:
        return exacto["id"]
    # parcial: gana la zona fronteriza, que es donde de verdad se practica
    parciales = [t for t in temas.values() if nombre in t["nombre"].lower()]
    parciales.sort(key=lambda t: t["bloque"] != "FR")
    return parciales[0]["id"] if parciales else None


def agrupar_por(filas, clave):
    grupos = defaultdict(list)
    for fila in filas:
        if fila.get(clave):
            grupos[fila[clave]].append(fila)
    return grupos


def sesiones_del_tema(tema_id, sesiones, por_sesion, cfg, temas):
    """Sesiones de ese tema, de la más reciente a la más antigua, con su tasa."""
    minimo = cfg["minimo_respuestas_sesion_valida"]
    salida = []
    for ses in sorted(sesiones, key=lambda s: s.get("id", ""), reverse=True):
        if normalizar_tema(ses, temas) != tema_id:
            continue
        respuestas = [r for r in por_sesion.get(ses.get("id"), []) if not r.get("repaso")]
        t = tasa(respuestas)
        valida = len(respuestas) >= minimo
        if not valida and isinstance(ses.get("resultado"), dict):
            # sesión anterior a respuestas.jsonl: vale el recuento que quedó escrito
            res = ses["resultado"]
            if res.get("ejercicios"):
                t = res["aciertos"] / res["ejercicios"]
                valida = True
        salida.append({
            "id": ses.get("id"),
            "fecha": ses.get("fecha"),
            "formato": ses.get("formato"),
            "ritmo": ses.get("ritmo"),
            "n_respuestas": len(respuestas),
            "tasa": round(t, 3) if t is not None else None,
            "valida": valida,
        })
    return salida


def esta_consolidado(historial, cfg):
    validas = [s for s in historial if s["valida"]][: cfg["sesiones_para_consolidar"]]
    return (
        len(validas) >= cfg["sesiones_para_consolidar"]
        and all(s["tasa"] is not None and s["tasa"] >= cfg["umbral_consolidacion"] for s in validas)
    )


def sugerir_formato(historial, temas, tema_id):
    """Rota el formato si el tema se repite; la amplitud decide si cabe identificar-error."""
    if not tema_id:
        return None, "según el tema que elijas: cerrado → completar / opciones; amplio → identificar-error"
    amplio = temas.get(tema_id, {}).get("amplitud") == "amplio"
    ultimos = [s["formato"] for s in historial[:2] if s.get("formato")]
    if len(ultimos) >= 2 and ultimos[0] == ultimos[1]:
        pool = FORMATOS_ROTACION + (["identificar-error"] if amplio else [])
        alternativas = [f for f in pool if f != ultimos[0]]
        return alternativas[0], f"dos sesiones seguidas en {ultimos[0]}, toca cambiar de formato"
    if ultimos:
        if ultimos[0] == "identificar-error" and not amplio:
            return "completar", "identificar-error no rinde en un tema cerrado"
        return ultimos[0], "el de la última sesión con este tema"
    return ("identificar-error", "tema amplio, sin historial") if amplio else \
           ("completar", "tema cerrado, sin historial")


def calcular():
    verificar_datos()
    cfg = config()
    temas = catalogo()
    sesiones = [s for s in leer_jsonl(SESIONES) if s.get("tipo") != "repaso"]
    respuestas = leer_jsonl(RESPUESTAS)
    for fila in respuestas + sesiones:
        fila["tema_id"] = normalizar_tema(fila, temas)

    del_tema = [r for r in respuestas if not r.get("repaso")]
    por_sesion = agrupar_por(respuestas, "sesion")

    por_tema = {k: resumen(v, temas) for k, v in agrupar_por(del_tema, "tema_id").items()}
    por_subtema = {k: resumen(v, temas) for k, v in agrupar_por(del_tema, "subtema_id").items()}
    por_formato = {k: resumen(v, temas) for k, v in agrupar_por(del_tema, "formato").items()}
    for tid, d in list(por_tema.items()) + list(por_subtema.items()):
        d["nombre"] = temas.get(tid, {}).get("nombre", tid)

    umbral = cfg["umbral_consolidacion"]
    necesarias = cfg["sesiones_para_consolidar"]

    ultima = max(sesiones, key=lambda s: s.get("id", "")) if sesiones else None
    tema_actual = ultima.get("tema_id") if ultima else None
    historial = sesiones_del_tema(tema_actual, sesiones, por_sesion, cfg, temas) if tema_actual else []
    consolidado = esta_consolidado(historial, cfg)

    # temas consolidados en todo el histórico: no se vuelven a sugerir
    consolidados = {
        tid for tid in por_tema
        if esta_consolidado(sesiones_del_tema(tid, sesiones, por_sesion, cfg, temas), cfg)
    }

    # puntos flojos: subtemas con muestra suficiente por debajo del umbral, peor primero
    flojos = sorted(
        ((tid, d) for tid, d in por_subtema.items() if d["n"] >= 3 and d["tasa"] < umbral),
        key=lambda kv: kv[1]["tasa"],
    )
    flojos_del_tema = [
        tid for tid, _ in flojos
        if any(r.get("subtema_id") == tid and r.get("tema_id") == tema_actual for r in del_tema)
    ]

    if not tema_actual:
        sugerencia = {
            "tema_id": None,
            "motivo": "primera sesión — elige un id del bloque FR (zona fronteriza B1→B2)",
        }
    elif not consolidado:
        if flojos_del_tema:
            punto = flojos_del_tema[0]
            d = por_subtema[punto]
            dentro = "" if punto == tema_actual else \
                f" dentro de «{temas.get(tema_actual, {}).get('nombre', tema_actual)}»"
            sugerencia = {
                "tema_id": punto,
                "motivo": f"sigue flojo{dentro}: {d['tasa']:.0%} en {d['n']} ítems",
            }
        else:
            hechas = len([s for s in historial if s["valida"]])
            sugerencia = {
                "tema_id": tema_actual,
                "motivo": f"{hechas} sesión(es) válida(s) con este tema, "
                          f"aún sin {necesarias} por encima del {umbral:.0%}",
            }
    else:
        candidato = next((tid for tid, _ in flojos if tid not in consolidados), None)
        sugerencia = {
            "tema_id": candidato,
            "motivo": f"«{temas.get(tema_actual, {}).get('nombre', tema_actual)}» consolidado "
                      f"({necesarias} sesiones ≥ {umbral:.0%}) — "
                      + ("toca el punto más flojo pendiente" if candidato
                         else "toca un id del bloque FR de los que siguen sin tocar"),
        }

    # el formato se decide sobre el historial del tema **sugerido**, no del anterior
    hist_sugerido = (
        historial if sugerencia["tema_id"] == tema_actual
        else sesiones_del_tema(sugerencia["tema_id"], sesiones, por_sesion, cfg, temas)
        if sugerencia["tema_id"] else []
    )
    formato, motivo_formato = sugerir_formato(hist_sugerido, temas, sugerencia["tema_id"])
    sug_tema = temas.get(sugerencia["tema_id"], {})
    sugerencia.update({
        "tema": sug_tema.get("nombre"),
        "amplitud": sug_tema.get("amplitud"),
        "formato": formato,
        "motivo_formato": motivo_formato,
        "nivel": cfg["nivel"],
        "nivel_origen": "config.json — no se pregunta",
        "ritmo": (ultima or {}).get("ritmo") or cfg["ritmo_por_defecto"],
        "tema_anterior_id": tema_actual,
        "consolidado": consolidado,
    })

    return {
        "global": resumen(del_tema, temas),
        "repaso": resumen([r for r in respuestas if r.get("repaso")], temas),
        "por_tema": dict(sorted(por_tema.items(), key=lambda kv: kv[1]["tasa"])),
        "por_subtema": dict(sorted(por_subtema.items(), key=lambda kv: kv[1]["tasa"])),
        "por_formato": por_formato,
        "consolidados": sorted(consolidados),
        "sin_tocar": sorted(t for t in temas if t not in por_tema),
        "sesiones_tema_actual": historial,
        "sugerencia": sugerencia,
    }


def imprimir(datos):
    print(f"Datos: {DATA}")
    g = datos["global"]
    if not g["n"]:
        print("Sin respuestas registradas todavía.")
    else:
        print(f"Global: {g['aciertos']}/{g['n']} ({g['tasa']:.0%})"
              + (f", {g['parciales']} parciales" if g["parciales"] else ""))

    for titulo, clave in (("Por tema", "por_tema"), ("Puntos flojos", "por_subtema")):
        if datos[clave]:
            print(f"\n{titulo}:")
            for tid, d in datos[clave].items():
                print(f"  {d['tasa']:>5.0%}  {d['aciertos']:>3}/{d['n']:<3}  {tid:<42} {d['nombre']}")

    if datos["por_formato"]:
        print("\nPor formato:")
        for nombre, d in datos["por_formato"].items():
            print(f"  {d['tasa']:>5.0%}  {d['aciertos']:>3}/{d['n']:<3}  {nombre}")

    if datos["consolidados"]:
        print("\nConsolidados (no se vuelven a sugerir): " + ", ".join(datos["consolidados"]))

    if datos["sesiones_tema_actual"]:
        print("\nSesiones del tema actual (reciente → antigua):")
        for s in datos["sesiones_tema_actual"]:
            t = f"{s['tasa']:.0%}" if s["tasa"] is not None else "—"
            marca = "" if s["valida"] else "  (a medias, no cuenta)"
            print(f"  {s['fecha']}  {t:>5}  {s['formato']}{marca}")

    s = datos["sugerencia"]
    print("\nSugerencia de apertura:")
    print(f"  tema    {s['tema_id'] or '(elige un id FR.* del catálogo)'}"
          + (f"  «{s['tema']}»" if s.get("tema") else ""))
    print(f"          {s['motivo']}")
    print(f"  formato {s['formato'] or '(sin decidir)'}  — {s['motivo_formato']}")
    print(f"  nivel   {s['nivel']}  — {s['nivel_origen']}")
    print(f"  ritmo   {s['ritmo']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--tema-id", help="restringe el informe a un tema")
    args = p.parse_args()
    datos = calcular()
    if args.tema_id:
        datos["por_tema"] = {k: v for k, v in datos["por_tema"].items() if k == args.tema_id}
    if args.json:
        print(json.dumps(datos, ensure_ascii=False, indent=2))
    else:
        imprimir(datos)
