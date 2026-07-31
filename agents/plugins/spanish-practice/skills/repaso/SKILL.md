---
name: repaso
description: Sesión de repaso espaciado sobre los ítems de español ya aprendidos y vencidos, 5–8 ejercicios, sin tema del día detrás. Use when the user says "repaso", "spaced repetition", asks to review previously learned Spanish items, or invokes /spanish-practice:repaso.
---

# `repaso` — sesión de repaso completa

`/spanish-practice:repaso`. Repaso explícito sobre los ítems vencidos de `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/aprendido.jsonl` — ruta absoluta a propósito: el plugin instalado se ejecuta desde una copia en caché versionada, y el registro tiene que vivir (y commitearse) en la copia de trabajo. Sin tema del día detrás. Aquí **no hay sorteo**: se hace siempre, con 5–8 ítems. Si no hay nada vencido, dilo y ofrece repasar lo más antiguo igualmente.

Algoritmo de selección, vencimientos y actualización de las líneas: `../../references/repaso.md`. Vale para los dos casos — el repaso explícito y la apertura de la skill `spanish-practice:practicar`.

## Skills hermanas

- **Sesión de ejercicios sobre un tema** → skill `spanish-practice:practicar`.
- **Apuntar algo nuevo** → skill `spanish-practice:recordar`.
