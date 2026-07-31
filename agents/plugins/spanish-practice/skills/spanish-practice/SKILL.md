---
name: spanish-practice
description: Genera ejercicios interactivos de español (opciones, texto libre, completar, identificar el error) sobre un tema dado, con feedback razonado, y abre la sesión con repaso espaciado cuando toca. Use when the user says "spanish practice", "ejercicios de español", "practicar español", asks to be quizzed on a Spanish topic (subjuntivo, ser/estar, español de México, B1…), or invokes /spanish-practice.
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

## Cómo se ejecuta la sesión

0. **Antes de nada, mira si toca repaso.** Lee `/Users/theo/.dotfiles/agents/plugins/spanish-practice/data/aprendido.jsonl` — ruta absoluta a propósito: el plugin instalado se ejecuta desde una copia en caché versionada, y el registro tiene que vivir (y commitearse) en la copia de trabajo. Si existe y tiene líneas, aplica la selección de `../../references/repaso.md`: hay ~70 % de probabilidad de abrir con **2–3 ítems ya aprendidos** en forma de ejercicio, antes del tema del día. Si el fichero no existe o está vacío, pasa al paso 1 sin decir nada.
1. Si toca repaso: sirve esos 2–3 ítems, corrige, actualiza sus líneas en el fichero y **transiciona en una frase** al tema pedido. Nada de resúmenes largos — la apertura es un calentamiento, no la sesión. Si el usuario dice "hoy no" o "sin repaso", salta directo al paso 2.
2. Confirma **tema**, **formato** y **nivel** en una línea. No pidas más datos de los necesarios.
3. Genera la tanda de ejercicios numerados. **No des las respuestas todavía.**
4. Espera a que el usuario responda. Puede responder a todos de golpe o de uno en uno; si responde de uno en uno, corrige ese ítem al momento y no esperes al resto.
5. Da feedback **ejercicio por ejercicio**:
   - ✅ / ❌ y la respuesta correcta.
   - **Por qué** es correcta — la regla, no solo la etiqueta.
   - **Por qué falla** lo que puso el usuario, si falló.
   - **Todas las demás formas gramaticales**, cada una con la lectura que la hace válida. Obligatorio, no opcional — ver "Regla del abanico completo".
6. Cierra con un resumen breve: qué domina, qué conviene repasar, y ofrece otra tanda (más difícil, mismo tema; o tema nuevo). Si en la sesión ha caído algún "ah, ahora lo veo", ofrece apuntarlo (skill `spanish-practice:recordar`).

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
