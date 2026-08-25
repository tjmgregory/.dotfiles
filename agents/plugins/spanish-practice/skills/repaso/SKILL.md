---
name: repaso
description: Sesión de repaso espaciado sobre los ítems de español ya aprendidos y vencidos, 5–8 ejercicios, sin tema del día detrás. Use when the user says "repaso", "spaced repetition", asks to review previously learned Spanish items, or invokes /spanish-practice:repaso.
---

# `repaso` — sesión de repaso completa

`/spanish-practice:repaso`. Repaso explícito sobre los ítems vencidos de `$SPANISH_PRACTICE_DATA/aprendido.jsonl` — la carpeta de datos es `~/.spanish-practice` salvo que `SPANISH_PRACTICE_DATA` la mueva, que es lo que hace `~/.zshenv` en esta máquina para mandarla a iCloud Drive. Los scripts la resuelven solos; vive fuera del repo a propósito. Sin tema del día detrás. Aquí **no hay sorteo**: se hace siempre, con 5–8 ítems. Si no hay nada vencido, dilo y ofrece repasar lo más antiguo igualmente.

**Ritmo:** por defecto **uno a uno** — un ejercicio por mensaje, corriges, y el siguiente sale en ese mismo mensaje detrás del feedback. Pregúntalo en la línea de apertura ("¿uno a uno o los 6 de golpe?") y respétalo si el usuario ya lo ha dicho. Detalle en "Ritmo de entrega" de la skill `spanish-practice:spanish-practice`.

Algoritmo de selección, vencimientos y actualización de las líneas: `../../references/repaso.md`. Vale para los dos casos — el repaso explícito y la apertura de la skill `spanish-practice:spanish-practice`.

## Registro de la sesión

Antes del primer ítem, abre la sesión con el script — aquí no hay tema del día, así que va sin `--tema-id` ni `--formato`:

```bash
cd /Users/theo/.dotfiles/agents/plugins/spanish-practice/scripts
python3 abrir_sesion.py --tipo repaso --ritmo uno-a-uno
```

**Cada ítem corregido se registra en el momento**, con el `tema_id` que trae el ítem de `aprendido.jsonl` y la marca `--repaso`, que lo deja fuera de las tasas del tema del día:

```bash
python3 registrar.py --sesion <id> --n 2/6 --tema-id FR.aunque-modo \
  --formato completar --correcto si --respuesta "…" --esperada "…" --repaso
```

Al cerrar, `python3 cerrar_sesion.py --sesion <id>`. Si la sesión se queda a medias, se queda sin `resultado` y así se queda. Esquema completo de los ficheros y del catálogo de ids: skill `spanish-practice:spanish-practice`.

## Skills hermanas

- **Sesión de ejercicios sobre un tema** → skill `spanish-practice:spanish-practice`.
- **Apuntar algo nuevo** → skill `spanish-practice:recordar`.
