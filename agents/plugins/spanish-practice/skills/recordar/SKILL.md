---
name: recordar
description: Apunta un ítem de español recién entendido en el registro de lo aprendido, con la formulación del propio usuario, para que entre en el repaso espaciado. Use when the user says "apúntalo", "recuerda esto", "guárdalo" mid-session, wants to mark a Spanish insight to remember, or invokes /spanish-practice:recordar.
---

# `recordar` — apuntar algo aprendido

`/spanish-practice:recordar <cosa>`, o a mitad de sesión cuando el usuario dice **"apúntalo"**, "recuerda esto", "guárdalo" o parecido. En ese caso el `<cosa>` es lo que se acaba de explicar; no preguntes cuál, dedúcelo del contexto inmediato.

Añade **una línea JSON** al final de `$SPANISH_PRACTICE_DATA/aprendido.jsonl` — la carpeta de datos es `~/.spanish-practice` salvo que `SPANISH_PRACTICE_DATA` la mueva, que es lo que hace `~/.zshenv` en esta máquina para mandarla a iCloud Drive. Los scripts la resuelven solos; vive fuera del repo a propósito.

```json
{"fecha": "2026-07-31", "item": "aunque + subjuntivo presenta el obstáculo como ya sabido y no discutido", "tema_id": "FR.aunque-modo", "tema": "Aunque + indicativo / subjuntivo", "nivel": "B1/B2", "notas": "el modo no dice si es verdad, dice si lo estoy poniendo sobre la mesa o dándolo por hecho", "repasos": [], "aciertos": 0, "sesion": "2026-07-31-2143"}
```

| campo | qué va |
|---|---|
| `fecha` | Día de hoy, `YYYY-MM-DD`. Sácalo con `date +%F` — **no lo deduzcas**. |
| `item` | Descripción corta de lo entendido. Una línea. |
| `tema_id` | **Id del catálogo oficial** (`../../references/temas.json`). Resuélvelo con `python3 ../../scripts/temas.py --buscar "aunque"`; no inventes uno. Es lo que enlaza este ítem con las tasas de acierto y con el tema que se practica. |
| `tema` | El `nombre` que trae ese id en el catálogo. Redundante a propósito: hace legible el fichero. |
| `nivel` | El `nivel` del id en el catálogo, no el del usuario. |
| `notas` | Opcional: la regla **como la formuló el usuario**. |
| `repasos` | `[]` en ítems nuevos. Fechas de repaso después. |
| `aciertos` | `0` en ítems nuevos. |
| `sesion` | Opcional: el `id` de la sesión abierta, tal como está en `sesiones.jsonl`. Si el "apúntalo" cae fuera de toda sesión, deja el campo fuera. |

**Lo que se apunta es el clic del usuario, no la regla del manual.** Si dijo "ah, entonces el subjuntivo aquí no es duda, es que no lo estoy afirmando", eso va en `notas` tal cual. Una reformulación de gramática académica no le va a devolver el recuerdo dentro de tres semanas; su propia frase sí. Si no hubo formulación propia, deja `notas` fuera antes que inventarla.

Confirma en una línea qué has apuntado y sigue con lo que estabais haciendo.

## Skills hermanas

- **Sesión de ejercicios** → skill `spanish-practice:spanish-practice`.
- **Repaso de lo apuntado** → skill `spanish-practice:repaso`. Cómo se seleccionan y actualizan las líneas: `../../references/repaso.md`.
