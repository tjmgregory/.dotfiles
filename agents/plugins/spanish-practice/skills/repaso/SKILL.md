---
name: repaso
description: Sesión de repaso espaciado sobre los ítems de español ya aprendidos y vencidos, 5–8 ejercicios, sin tema del día detrás. Use when the user says "repaso", "spaced repetition", asks to review previously learned Spanish items, or invokes /spanish-practice:repaso.
---

# `repaso` — sesión de repaso completa

`/spanish-practice:repaso`. Repaso explícito sobre los ítems vencidos de `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/aprendido.jsonl` — ruta absoluta a propósito: el plugin instalado se ejecuta desde una copia en caché versionada, y el registro tiene que vivir (y commitearse) en la copia de trabajo. Sin tema del día detrás. Aquí **no hay sorteo**: se hace siempre, con 5–8 ítems. Si no hay nada vencido, dilo y ofrece repasar lo más antiguo igualmente.

**Ritmo:** por defecto **uno a uno** — un ejercicio por mensaje, corriges, y el siguiente sale en ese mismo mensaje detrás del feedback. Pregúntalo en la línea de apertura ("¿uno a uno o los 6 de golpe?") y respétalo si el usuario ya lo ha dicho. Detalle en "Ritmo de entrega" de la skill `spanish-practice:spanish-practice`.

Algoritmo de selección, vencimientos y actualización de las líneas: `../../references/repaso.md`. Vale para los dos casos — el repaso explícito y la apertura de la skill `spanish-practice:spanish-practice`.

## Registro de la sesión

Antes del primer ítem, añade la línea de esta sesión a `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/sesiones.jsonl` (ruta absoluta por lo mismo) con `tipo` `"repaso"`: `tema` a `null` o fuera —aquí no hay tema del día—, `ritmo` como haya quedado, y sin `formato` ni `repaso_apertura`, que no pintan nada en un repaso. Al cerrar, reescribe esa línea añadiéndole `resultado`; si la sesión se queda a medias, se queda sin él. Esquema completo de la línea: skill `spanish-practice:spanish-practice`.

## Skills hermanas

- **Sesión de ejercicios sobre un tema** → skill `spanish-practice:spanish-practice`.
- **Apuntar algo nuevo** → skill `spanish-practice:recordar`.
