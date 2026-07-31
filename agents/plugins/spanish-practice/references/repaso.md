# Repaso espaciado — selección de ítems

Cómo se decide **si** hay repaso y **qué** se repasa. Todo el estado vive en `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/aprendido.jsonl`, una línea JSON por ítem aprendido — ruta absoluta a propósito: el plugin instalado se ejecuta desde una copia en caché versionada, y el registro tiene que vivir (y commitearse) en la copia de trabajo.

La fecha de hoy se obtiene siempre con `date +%F`. No la deduzcas.

---

## Intervalo por número de aciertos

Cada ítem tiene su propio ritmo según cuántas veces se ha repasado bien (`aciertos`):

| aciertos | intervalo |
|---|---|
| 0 | 2 días |
| 1 | 7 días |
| 2 | 21 días |
| 3 o más | 60 días |

La lógica es la de siempre en repaso espaciado: lo que ya sale solo no hace falta tocarlo, y lo recién entendido se cae rápido si no se vuelve a él en dos o tres días.

## Antigüedad de un ítem

**Días transcurridos** = hoy − última fecha de `repasos`. Si `repasos` está vacío, se cuenta desde `fecha` (el día en que se apuntó).

## Vencimiento

Compara días transcurridos contra el intervalo del ítem:

- **Muy vencido** — el doble del intervalo o más. Pesa **3**.
- **Vencido** — llega al intervalo pero no al doble. Pesa **2**.
- **Casi** — pasa de la mitad del intervalo. Pesa **1**.
- **Fresco** — por debajo de la mitad. No entra en el sorteo.

Los pesos son papeletas para el sorteo, no un orden. Un ítem casi vencido puede salir antes que uno muy vencido; es lo que evita que la sesión se vuelva predecible.

## Sorteo de apertura (70 %)

Solo si hay al menos un ítem no fresco. Elige un número al azar del 1 al 10:

- **1–7** → hay repaso de apertura.
- **8–10** → no lo hay, directo al tema del día.

No anuncies el sorteo ni lo comentes. Si sale que no, empieza el tema sin mencionar que había repaso pendiente.

En la skill `spanish-practice:repaso` **no hay sorteo**: el usuario lo ha pedido, se hace siempre y con más ítems.

## Elección de los ítems

1. Reparte papeletas: cada ítem aporta tantas como su peso (3 / 2 / 1).
2. Saca 2–3 ítems al azar del montón, sin repetir. En `repaso` explícito, 5–8.
3. Si dos ítems comparten `tema`, quédate con uno y saca otro — dos huecos del mismo punto gramatical en una apertura de tres es desaprovecharla.
4. Prioriza a igualdad de papeletas los de `nivel` B2: son los que más se caen.

## Forma del repaso

**Ejercicio, no interrogatorio.** Nada de "¿te acuerdas de la diferencia entre X e Y?" — eso mide reconocimiento, no uso. Monta un ítem real de los formatos habituales (completar, opciones, identificar el error) que obligue a aplicar la regla sin nombrarla.

Usa el campo `notas` para calibrar: ahí está la regla tal como la entendió el usuario. El ejercicio debe caer justo donde esa formulación se rompería si estuviera mal entendida.

No repitas la frase con la que se apuntó el ítem. Contexto nuevo, misma regla: si solo recuerda la frase, no ha aprendido nada.

Apertura corta — dos o tres ítems, feedback breve, y al tema del día. El abanico completo se aplica igual, pero comprimido; el repaso no es el plato principal.

## Después de corregir

Reescribe la línea de ese ítem en `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/aprendido.jsonl`:

- Añade la fecha de hoy a `repasos`, acierte o falle. Refleja cuándo se tocó por última vez.
- **Acierta** → `aciertos` + 1.
- **Falla** → `aciertos` vuelve a **0**. Si estaba mal entendida, el ítem arranca de cero: vuelve a los 2 días.
- Si al fallar se ve que la formulación de `notas` era la culpable, reescríbela con la corrección — en los términos del usuario, no en los de una gramática.

Reescribe **solo esa línea**; el resto del fichero se queda intacto.

## Saltar el repaso

"hoy no", "sin repaso", "vamos al tema" → salta la apertura sin discutir y no toques `repasos` de nada. No es un fallo, es que hoy no toca.
