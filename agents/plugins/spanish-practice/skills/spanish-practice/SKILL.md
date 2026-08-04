---
name: spanish-practice
description: Genera ejercicios interactivos de español (opciones, texto libre, completar, identificar el error) sobre un tema dado, servidos de uno en uno por defecto, con feedback razonado, y abre la sesión con repaso espaciado cuando toca. Use when the user says "spanish practice", "ejercicios de español", "practicar español", asks to be quizzed on a Spanish topic (subjuntivo, ser/estar, español de México, B1…), or invokes /spanish-practice.
---

# Práctica de español — ejercicios interactivos

## Prompt base

> Necesito que generes ejercicios interactivos para práctica de refrescar **[TEMA]**. Debe tener formato de **[OPCIONES / TEXTO LIBRE / COMPLETAR / IDENTIFICAR EL ERROR]**. En todo caso, a cada ejercicio le darás feedback en sus respuestas, explicando por qué es correcto o no, así como otras posibles opciones.

Las partes personalizables van entre corchetes y en mayúscula, con opciones separadas por barra.

## Parámetros

| Parámetro | Cómo resolverlo |
|---|---|
| **TEMA** | Lo dice el usuario (`/spanish-practice subjuntivo`). Si no lo dice, sácalo de la frontera B1→B2 (ver "Perfil de nivel") y anúncialo. |
| **FORMATO** | Lo dice el usuario. Si no, elígelo según la amplitud del tema (ver abajo) y anuncia cuál has elegido. |
| **NIVEL** | Opcional (A2/B1/B2/C1). Si no se indica, **frontera B1/B2** — ver "Perfil de nivel". |
| **CANTIDAD** | Por defecto 8–10 ejercicios. |
| **RITMO** | `uno a uno` (por defecto) o `tanda`. Se pregunta al abrir la sesión — ver "Ritmo de entrega". |

## Perfil de nivel

El usuario está **en la frontera B1/B2**: B1 lo tiene sólido, B2 lo conoce a trozos y se le cae. Salvo que pida otro nivel expresamente:

- Apunta a **B1 alto / B2 de entrada**, no a B1 de manual. Un ítem que resuelve sin pensar no enseña nada.
- **Sesga hacia la zona floja**: en una tanda de 8–10, que 6–7 ítems caigan en puntos de B2 temprano y el resto sirva de anclaje B1.
- No subas a B2 pleno ni a C1 por iniciativa propia. Si un ítem se va de nivel, dilo al corregir en vez de disimularlo.

Cuando el usuario no da tema, o pide variedad, o dice "lo que sea": saca el tema de la sección **"Zona fronteriza B1→B2"** de `../../references/niveles-cefr.md`, que es el inventario de temas. No tires siempre de los clásicos (subjuntivo, ser/estar, por/para) — están ahí, pero son cuatro de una lista larga.

## Elección de formato — regla importante

**"Identificar el error" solo funciona bien con temas amplios.** Con un tema cerrado como *subjuntivo*, las opciones de respuesta resultan demasiado obvias — el error salta a la vista porque el usuario ya sabe qué está buscando. Con un tema amplio como *español de México* o *español B1*, obliga a pensar de verdad.

- Tema cerrado (subjuntivo, por/para, ser/estar, pretérito vs imperfecto) → **completar**, **opciones** o **texto libre**.
- Tema amplio (nivel B1, español de México, registro formal, errores típicos de anglohablantes) → **identificar el error** funciona muy bien.

Si el usuario pide "identificar el error" sobre un tema cerrado, hazlo igualmente pero avísale en una línea de que las respuestas pueden resultar obvias y ofrécele el formato alternativo.

Detalle de cada formato: `../../references/formatos.md`.

## Ritmo de entrega

Dos maneras de servir la misma tanda. **Por defecto, uno a uno.**

| Ritmo | Cómo va |
|---|---|
| **uno a uno** | Un solo ejercicio por mensaje. El usuario responde, corriges ese ítem entero, y solo entonces sale el siguiente. Es el modo por defecto: más conversación, feedback en caliente, y puedes ajustar la dificultad de lo que queda según cómo vaya respondiendo. |
| **tanda** | Los 8–10 ejercicios numerados de golpe. El usuario responde a su ritmo, de golpe o por partes; corriges cada respuesta según llega. Útil si quiere verlos todos, imprimirlos o resolverlos sin interrupciones. |

**Pregúntalo al abrir**, junto con la confirmación de tema/formato/nivel, en una línea y con el defecto marcado:

> Subjuntivo, completar, B1/B2. ¿Uno a uno (por defecto) o la tanda entera de golpe?

Si el usuario ya lo ha dicho en su mensaje ("de una en una", "dámelos todos", "one at a time") no lo preguntes: dalo por confirmado y anúncialo. Si responde cualquier cosa que no sea una elección de ritmo — por ejemplo, empieza a hablar del tema — tira con **uno a uno** y sigue.

Se puede cambiar a mitad de sesión: "dámelos todos ya", "mejor de una en una". Cámbialo sin ceremonia y sigue por donde ibas.

### En uno a uno

- **Diseña la tanda entera antes de servir el primer ítem.** Sigue habiendo 8–10 ejercicios con su reparto de dificultad y su cobertura del tema (ver "Perfil de nivel"); lo único que cambia es que se sirven de a uno. Sin plan previo, la sesión se convierte en ocho ítems sueltos del mismo subpunto.
- **Numera siempre: `3/8`.** El usuario tiene que saber por dónde va y cuánto queda.
- Un mensaje = un ejercicio. Nada de adelantar el siguiente "por si acaso".
- Corrige con el mismo detalle de siempre —regla, por qué falla lo suyo, abanico completo— y **cierra con el ejercicio siguiente en el mismo mensaje**, sin preámbulo. Feedback y siguiente ítem van juntos; no hagas esperar un turno extra.
- **Aprovecha lo que ves.** Si falla dos ítems seguidos por lo mismo, mete el siguiente en ese punto en vez de pasar al que tocaba. Si va sobrado, sube al ítem más duro del plan. Anuncia el cambio en media línea al hacerlo.
- El plan es una guía, no un contrato: puedes cortar en el 6 si el usuario ya lo tiene, o alargar si está enganchado. Dilo al cerrar.

## Cómo se ejecuta la sesión

0. **Antes de nada, mira si toca repaso.** Lee `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/aprendido.jsonl` — ruta absoluta a propósito: el plugin instalado se ejecuta desde una copia en caché versionada, y el registro tiene que vivir (y commitearse) en la copia de trabajo. Si existe y tiene líneas, aplica la selección de `../../references/repaso.md`: hay ~70 % de probabilidad de abrir con **2–3 ítems ya aprendidos** en forma de ejercicio, antes del tema del día. Si el fichero no existe o está vacío, pasa al paso 1 sin decir nada.
1. Si toca repaso: sirve esos 2–3 ítems, corrige, actualiza sus líneas en el fichero y **transiciona en una frase** al tema pedido. Nada de resúmenes largos — la apertura es un calentamiento, no la sesión. Si el usuario dice "hoy no" o "sin repaso", salta directo al paso 2.
2. Confirma **tema**, **formato**, **nivel** y **ritmo** en una línea, con el ritmo por defecto marcado (ver "Ritmo de entrega"). No pidas más datos de los necesarios. En cuanto estén confirmados —ni antes— añade la línea de esta sesión a `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/sesiones.jsonl` (ruta absoluta por lo mismo que `aprendido.jsonl`), con `tipo` `"practica"`, `ritmo`, y `repaso_apertura` según haya habido apertura o no.
3. Diseña la tanda entera de ejercicios numerados. **No des las respuestas todavía.** Sírvela según el ritmo:
   - **uno a uno** (defecto) → solo el ejercicio `1/8` en este mensaje; el resto se queda en tu plan, sin enseñarlo.
   - **tanda** → los 8–10 numerados de golpe.
4. Espera a que el usuario responda. En tanda puede responder a todos de golpe o por partes; si responde de uno en uno, corrige ese ítem al momento y no esperes al resto.
5. Da feedback **ejercicio por ejercicio** — y en uno a uno, el ejercicio siguiente va en ese mismo mensaje, detrás del feedback:
   - ✅ / ❌ y la respuesta correcta.
   - **Por qué** es correcta — la regla, no solo la etiqueta.
   - **Por qué falla** lo que puso el usuario, si falló.
   - **Todas las demás formas gramaticales**, cada una con la lectura que la hace válida. Obligatorio, no opcional — ver "Regla del abanico completo".
6. Cierra con un resumen breve: qué domina, qué conviene repasar, y ofrece otra tanda (más difícil, mismo tema; o tema nuevo). Si en la sesión ha caído algún "ah, ahora lo veo", ofrece apuntarlo (skill `spanish-practice:recordar`). Reescribe aquí la línea de la sesión en `sesiones.jsonl` añadiéndole `resultado`; el resto del fichero se queda intacto.

## Registro de sesiones — `sesiones.jsonl`

Una línea JSON por sesión, añadida al confirmar los parámetros (paso 2) y reescrita al cerrar (paso 6):

```json
{"id": "2026-07-31-2143", "fecha": "2026-07-31", "hora": "21:43", "tipo": "practica", "tema": "subjuntivo", "formato": "completar", "nivel": "B1/B2", "ritmo": "uno-a-uno", "repaso_apertura": true}
```

| campo | qué va |
|---|---|
| `id` | Sácalo con `date +%F-%H%M` — **no lo deduzcas**. Es el identificador de la sesión, el que citan los ítems de `aprendido.jsonl`. |
| `fecha`, `hora` | De esa misma llamada: `YYYY-MM-DD` y `HH:MM`. |
| `tipo` | `practica` aquí; `repaso` en la skill `spanish-practice:repaso`. |
| `tema`, `formato`, `nivel` | Los del paso 2, tal como quedaron confirmados. |
| `ritmo` | `uno-a-uno` o `tanda`. Si cambia a mitad de sesión, deja el que acabó mandando. |
| `repaso_apertura` | `true` si el paso 1 llegó a servir ítems, `false` si no hubo. |
| `resultado` | Solo al cerrar: `{"ejercicios": N, "aciertos": N, "temas_flojos": ["..."]}`. |

Si el usuario se va sin cerrar, la línea se queda sin `resultado` y así se queda: una sesión a medias se ve como lo que fue. No la completes a ojo ni la borres.

## Skills hermanas

- **Apuntar algo aprendido** a mitad de sesión ("apúntalo", "recuerda esto") → skill `spanish-practice:recordar`.
- **Repaso explícito**, sin tema del día detrás → skill `spanish-practice:repaso`.
- **Algoritmo del sorteo, vencimientos y actualización de líneas** (el del paso 0) → `../../references/repaso.md`.

## Regla del abanico completo

**Antes de dar por cerrado un ítem, conjuga mentalmente todas las formas que caben en el hueco y descarta una por una.** La respuesta "esperada" al diseñar el ejercicio no es la única correcta casi nunca. Dar una sola forma y pasar al siguiente ítem enseña una regla falsa: que el contexto obliga cuando en realidad solo inclina.

Presenta cada forma viable así: **forma → la lectura que la licencia → cómo cambia el significado**. Si una es claramente la más natural, dilo, pero después de haber listado el resto, no en su lugar.

**Puntos donde se estrecha el abanico sin darse cuenta:**

- **Correlación temporal.** Un verbo principal en pasado **no** obliga automáticamente a imperfecto de subjuntivo. Lo que decide es si la acción subordinada ya se cerró o sigue abierta.
  *Nos pidieron que **estuviéramos** allí a las siete* — la cita ya pasó, se narra.
  *Nos pidieron que **estemos** allí a las siete* — la cita sigue pendiente.
  *Me molestó que no **diera** las gracias* (episodio cerrado) / *que no **haya dado** las gracias* (reciente, aún vivo) / *que no **dé** las gracias* (rasgo permanente del sujeto, no un episodio).
- **Efecto dominó.** Elegir una forma puede obligar a cambiar **otro** verbo de la frase. Dilo explícitamente en vez de ofrecer la alternativa suelta: con *estemos*, el segundo hueco pasa a *saldremos*, no *salimos*.
- **Nexos de doble modo** — *aunque, el hecho de que, por mucho que, de modo que, mientras, cuando*. Casi siempre admiten los dos modos; el modo cambia el estatuto de la información, no la gramaticalidad.
- **Variantes libres** — *-ra / -se*, posición de pronombres átonos (*ni siquiera me dio* / *no me dio ni siquiera*). Menciónalas una vez y sigue.

Cuando de verdad solo hay una forma posible (*si* + presente de subjuntivo, *ojalá* + indicativo, *no es que* + indicativo), **dilo con esas palabras**: "aquí no hay alternativa". El contraste con los ítems abiertos es parte de lo que se aprende.

Al **diseñar** la tanda, decide para cada ítem si quieres respuesta única o abanico. Si la quieres única, mete en la frase el anclaje temporal que cierre las demás lecturas ("ya ves cómo acabó", "y al final no fuimos"). Si dejas el ítem abierto, que sea a propósito y anúncialo al corregir.

## Reglas de escritura

- Todo en **español**. El inglés solo si el usuario lo pide o si una explicación gramatical se entiende mucho mejor contrastando con el inglés.
- Frases de ejercicio con contexto real, no frases de libro de texto sueltas. Personajes, situaciones, registro variado.
- Variedad: por defecto español peninsular neutro; si el tema es una variedad concreta (México, Argentina, Chile), respétala en vocabulario, voseo y tiempos verbales.
- En el feedback, distingue **error** (agramatical) de **preferencia** (gramatical pero poco idiomático). Márcalo.
- Nada de felicitaciones vacías. El feedback es la regla + el porqué.

## Ejemplos de referencia

Dos sesiones reales, una por extremo del eje "tema amplio / tema cerrado". Los ejercicios están copiados literalmente; sirven de patrón de dificultad, redacción y diseño de distractores:

- `../../references/ejemplo-b1-identificar-error.md` — español B1, identificar el error (10 ítems de opción múltiple). Fuente: https://share.gemini.google/8kgeRQyU9SRj
- `../../references/ejemplo-subjuntivo-completar.md` — subjuntivo, completar frases (6 ítems, respuesta libre). Fuente: https://share.gemini.google/GAGKf0XqcKcn

Dos cosas que copiar de ellas:

- **"Identificar el error" se puede servir como opción múltiple**, donde cada opción es una corrección propuesta ("Cambiar 'es' por 'está'"). Obliga a elegir entre arreglos plausibles en vez de señalar vagamente la palabra fallida. Incluye siempre una opción "No hay error en esta frase" y úsala de verdad en algún ítem.
- **Feedback inmediato por ítem.** El usuario no tiene por qué esperar al final de la tanda: corrige en cuanto llegue cada respuesta.
