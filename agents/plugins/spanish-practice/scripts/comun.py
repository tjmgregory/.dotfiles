"""Rutas, config y lectura/escritura de los .jsonl del plugin.

Dos sitios distintos, a propósito:

- **El código y el catálogo** viven en el plugin (`~/.dotfiles/...`), versionados en git.
  Se ejecutan desde una copia en caché, así que las rutas al plugin son absolutas.
- **Los datos y la config personal** viven fuera del repo. Por defecto en
  `~/.spanish-practice`, que no depende de ningún sistema operativo ni de ningún
  servicio de sincronización. Para que sobrevivan a que muera la máquina, se apunta
  `SPANISH_PRACTICE_DATA` a una carpeta sincronizada; en esta máquina, desde
  `~/.zshenv` a iCloud Drive.

Si la variable no está puesta y el sitio por defecto está vacío mientras hay datos
en una carpeta sincronizada conocida, los scripts **se paran**: arrancar un historial
nuevo en paralelo al bueno es peor que fallar.
"""

import json
import os
from pathlib import Path

BASE = Path(
    os.environ.get(
        "SPANISH_PRACTICE_DIR",
        "/Users/theo/.dotfiles/agents/plugins/spanish-practice",
    )
)
TEMAS_PATH = BASE / "references" / "temas.json"
DEFAULTS_PATH = BASE / "config.defaults.json"

POR_DEFECTO = Path.home() / ".spanish-practice"
DATA = Path(os.environ.get("SPANISH_PRACTICE_DATA", POR_DEFECTO)).expanduser()
CONFIG_PATH = DATA / "config.json"

# Sitios sincronizados donde el historial podría estar si la variable se ha perdido.
CANDIDATOS = [
    Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "spanish-practice",
    Path.home() / "Documents" / "spanish-practice",
]

SESIONES = DATA / "sesiones.jsonl"
RESPUESTAS = DATA / "respuestas.jsonl"
APRENDIDO = DATA / "aprendido.jsonl"

CONFIG_POR_DEFECTO = {
    "nivel": "B1/B2",
    "variedad": "peninsular neutro",
    "cantidad_ejercicios": [8, 10],
    "ritmo_por_defecto": "uno-a-uno",
    "umbral_consolidacion": 0.8,
    "sesiones_para_consolidar": 2,
    "minimo_respuestas_sesion_valida": 5,
}


def _tiene_historial(carpeta):
    return carpeta.is_dir() and any(carpeta.glob("*.jsonl"))


def verificar_datos():
    """Evita arrancar un historial nuevo en paralelo a uno que ya existe.

    Salta solo cuando se está usando el sitio por defecto, está vacío, y hay datos
    en una carpeta sincronizada conocida: señal de que `SPANISH_PRACTICE_DATA` se ha
    quedado sin poner en este shell.
    """
    if os.environ.get("SPANISH_PRACTICE_DATA") or _tiene_historial(DATA):
        return
    otros = [c for c in CANDIDATOS if c != DATA and _tiene_historial(c)]
    if not otros:
        return
    raise SystemExit(
        f"SPANISH_PRACTICE_DATA no está puesta, así que se usaría {DATA}, que está vacío,\n"
        f"pero ya hay historial en:\n  " + "\n  ".join(str(o) for o in otros) + "\n\n"
        "No se escribe nada para no partir el historial en dos. Arréglalo con:\n"
        f'  export SPANISH_PRACTICE_DATA="{otros[0]}"\n'
        "y déjalo puesto en ~/.zshenv (no en .zshrc: Claude Code usa un shell no interactivo)."
    )


def _leer_json(path, etiqueta):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{etiqueta} no es JSON válido: {exc}")


def config():
    """Defaults del repo, pisados por la config personal (que no está versionada)."""
    cfg = dict(CONFIG_POR_DEFECTO)
    if DEFAULTS_PATH.exists():
        cfg.update(_leer_json(DEFAULTS_PATH, DEFAULTS_PATH.name))
    if CONFIG_PATH.exists():
        cfg.update(_leer_json(CONFIG_PATH, str(CONFIG_PATH)))
    return cfg


def catalogo():
    """Los temas oficiales, indexados por id. Es la única lista válida de temas."""
    if not TEMAS_PATH.exists():
        raise SystemExit(f"falta el catálogo de temas en {TEMAS_PATH}")
    datos = json.loads(TEMAS_PATH.read_text(encoding="utf-8"))
    return {t["id"]: t for t in datos["temas"]}


def exigir_tema(tema_id):
    """Valida un id contra el catálogo. Sin id válido no se registra nada."""
    temas = catalogo()
    if tema_id in temas:
        return temas[tema_id]
    parecidos = [
        t for t in temas
        if tema_id.lower() in t.lower()
        or tema_id.lower() in temas[t]["nombre"].lower()
    ]
    pista = "\n  ".join(f"{t}  — {temas[t]['nombre']}" for t in parecidos[:8])
    raise SystemExit(
        f"«{tema_id}» no es un id del catálogo (references/temas.json)."
        + (f"\n¿Querías alguno de estos?\n  {pista}" if pista
           else "\nLista completa: python3 temas.py --listar")
    )


def leer_jsonl(path):
    """Líneas válidas de un .jsonl. Las corruptas se ignoran, no rompen."""
    if not path.exists():
        return []
    filas = []
    for linea in path.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            filas.append(json.loads(linea))
        except json.JSONDecodeError:
            continue
    return filas


def anadir_jsonl(path, fila):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(fila, ensure_ascii=False) + "\n")


def reescribir_linea(path, clave, valor, nueva_fila):
    """Sustituye la única fila con fila[clave] == valor. Deja el resto intacto."""
    filas = leer_jsonl(path)
    encontrada = False
    for i, fila in enumerate(filas):
        if fila.get(clave) == valor:
            filas[i] = nueva_fila
            encontrada = True
            break
    if not encontrada:
        raise SystemExit(f"no hay ninguna fila con {clave}={valor!r} en {path.name}")
    path.write_text(
        "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in filas),
        encoding="utf-8",
    )
