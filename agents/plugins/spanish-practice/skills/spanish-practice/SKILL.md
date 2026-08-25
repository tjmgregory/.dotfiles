---
name: spanish-practice
description: Genera ejercicios interactivos de español (opciones, texto libre, completar, identificar el error), servidos de uno en uno por defecto y con feedback razonado. Abre preguntando tema, formato y ritmo con una sugerencia calculada desde el histórico de aciertos, insistiendo en el mismo tema hasta consolidarlo. Use when the user says "spanish practice", "ejercicios de español", "practicar español", asks to be quizzed on a Spanish topic (subjuntivo, ser/estar, español de México, B1…), or invokes /spanish-practice.
---

# Práctica de español — ejercicios interactivos

## Prompt base

> Necesito que generes ejercicios interactivos para práctica de refrescar **[TEMA]**. Debe tener formato de **[OPCIONES / TEXTO LIBRE / COMPLETAR / IDENTIFICAR EL ERROR]**. En todo caso, a cada ejercicio le darás feedback en sus respuestas, explicando por qué es correcto o no, así como otras posibles opciones.

Las partes personalizables van entre corchetes y en mayúscula, con opciones separadas por barra.

## Parámetros

Lo que se negocia con el usuario **se pregunta**, con una sugerencia calculada ya puesta. Lo que es perfil o política **no se pregunta**: sale de `$SPANISH_PRACTICE_DATA/config.json`.

| Parámetro | Cómo resolverlo |
|---|---|
| **TEMA** | **Se pregunta.** Siempre un **id del catálogo** (`FR.valores-de-se`), nunca texto libre — ver "Catálogo de temas". Lo dice el usuario → tradúcelo a id con `temas.py --buscar` y confírmalo. Si no lo dice, pregúntalo con el id que sugiera `estadisticas.py`. |
| **FORMATO** | **Se pregunta**, con la sugerencia de `estadisticas.py`, que ya aplica la amplitud del tema (ver "Elección de formato"). |
| **RITMO** | **Se pregunta**: `uno a uno` o `tanda`, con la sugerencia del historial — ver "Ritmo de entrega". |
| **NIVEL** | **No se pregunta.** Es un dato de perfil: `config.json` → `nivel`. Solo cambia si el usuario pide expresamente otro nivel, y ese cambio va al fichero, no a la conversación. |
| **CANTIDAD** | No se pregunta: `config.json` → `cantidad_ejercicios` (8–10). |

## Perfil de nivel

**El nivel es un dato de perfil, no una pregunta.** Vive en `$SPANISH_PRACTICE_DATA/config.json` (`"nivel": "B1/B2"`) y de ahí lo leen los scripts. No lo preguntes al abrir ni lo deduzcas de cómo vaya la sesión: si el usuario pide otro nivel, edita el fichero y dilo en una línea.

El usuario está **en la frontera B1/B2**: B1 lo tiene sólido, B2 lo conoce a trozos y se le cae. Salvo que pida otro nivel expresamente:

- Apunta a **B1 alto / B2 de entrada**, no a B1 de manual. Un ítem que resuelve sin pensar no enseña nada.
- **Sesga hacia la zona floja**: en una tanda de 8–10, que 6–7 ítems caigan en puntos de B2 temprano y el resto sirva de anclaje B1.
- No subas a B2 pleno ni a C1 por iniciativa propia. Si un ítem se va de nivel, dilo al corregir en vez de disimularlo.

Cuando toque **proponer un tema nuevo** o el usuario pida variedad: sale del bloque `FR` del catálogo, que es la zona fronteriza B1→B2. No tires siempre de los clásicos (subjuntivo, ser/estar, por/para) — están ahí, pero son cuatro de una lista de 103.

## Catálogo de temas — los ids mandan

Los temas no son texto libre. Están enumerados en `../../references/temas.json`, derivados del **inventario del PCIC** (gramática, funciones y nociones B1/B2) que documenta `../../references/niveles-cefr.md`. Cada uno tiene un **id estable**:

| bloque | qué es | ejemplo |
|---|---|---|
| `G.B1.*` / `G.B2.*` | gramática del inventario PCIC | `G.B2.condicionales-irreales` |
| `F.B1.*` / `F.B2.*` | funciones comunicativas | `F.B2.argumentacion` |
| `LX.*` | léxico y nociones | `LX.B2.capa-abstracta` |
| `FR.*` | los 20 puntos de la zona fronteriza B1→B2 | `FR.valores-de-se` |

Cada entrada trae `nivel`, `amplitud` (`cerrado` / `amplio`, que decide el formato) y, si procede, el `FR.*` con el que enlaza.

```bash
cd /Users/theo/.dotfiles/agents/plugins/spanish-practice/scripts
python3 temas.py --buscar "valores de se"     # texto del usuario → id
python3 temas.py --listar --bloque FR         # la zona fronteriza entera
```

**Todo lo que se guarda va por id**: sesiones, respuestas y estadísticas. Los scripts rechazan un id que no esté en el catálogo, y en el error te proponen los parecidos. Si un tema que el usuario quiere no existe en el catálogo, añádelo al JSON con su bloque y su nivel — no lo metas como texto suelto.

## Apertura: preguntar con sugerencia

**Nada se elige a espaldas del usuario.** Tema, formato y ritmo se preguntan al abrir, los tres en un solo mensaje, cada uno con una sugerencia ya puesta. El nivel no se pregunta (sale de `config.json`). El usuario contesta solo lo que quiera cambiar; el resto va como está sugerido. Lo que ya venga en su mensaje (`/spanish-practice subjuntivo`, "de una en una") no se pregunta: se da por confirmado y se marca como tal.

**La sugerencia no la improvisas tú: la calcula un script.**

```bash
cd /Users/theo/.dotfiles/agents/plugins/spanish-practice/scripts
python3 estadisticas.py          # informe + sugerencia, legible
python3 estadisticas.py --json   # lo mismo, para leerlo con precisión
```

Devuelve tasa global, tasa por tema y por subtema, temas ya consolidados, temas sin tocar, y el bloque `sugerencia` con `tema_id`, `motivo`, `formato`, `motivo_formato`, `nivel` y `ritmo`. **Usa esos valores tal cual.** No recalcules a ojo ni "ajustes" la sugerencia: si el resultado no te convence, el que está mal es el umbral de `config.json`, y eso se cambia en el fichero.

### Regla del tema: insistir antes de rotar

Cambiar de tema cada sesión es lo que impide que nada se consolide. **Por defecto se repite el tema de la última sesión.** El script la implementa así, con los umbrales de `config.json`:

- Una sesión cuenta como evidencia si tiene al menos `minimo_respuestas_sesion_valida` respuestas registradas. **Las abandonadas a medias no cuentan** — repetir tema.
- Un tema queda **consolidado** cuando las **`sesiones_para_consolidar` últimas válidas** están todas en `umbral_consolidacion` o por encima (2 sesiones ≥ 80 % de serie). Solo entonces rota, y no vuelve a sugerirlo.
- Mientras no esté consolidado, se repite. Si dentro del tema hay un **subtema** por debajo del umbral con al menos 3 ítems, se sugiere **ese punto estrecho** en su lugar: misma insistencia, mejor apuntada.
- Al rotar, el candidato es el punto más flojo pendiente; si no hay ninguno, toca un `FR.*` sin tocar (`sin_tocar` en la salida).

Excepciones, sin discutir: el usuario nombra un tema, dice "cambia de tema", "estoy harto de esto" o similar → se hace lo que pide. Insistir es el defecto, no una imposición.

### Formato y ritmo

Vienen ya resueltos en `sugerencia`. Lo que hace el script: el formato es el de la última sesión con **ese** tema; si el tema se repite dos veces con el mismo formato, rota a otro; y filtra `identificar-error` según la `amplitud` del tema. El ritmo es el de la última sesión. Tú solo los presentas con su motivo.

### Forma del mensaje

Compacto, tres líneas de parámetro, sugerencia en negrita. Nada de párrafos de introducción:

> La última fue **valores de se** y quedó al 50 % — repetimos.
> - **Tema**: valores de se (`FR.valores-de-se`)
> - **Formato**: opciones (las dos últimas fueron completar)
> - **Ritmo**: uno a uno
>
> ¿Cambio algo, o tiro con esto?

El nivel no aparece en la lista: no es una pregunta. Si el usuario responde cualquier cosa que no sea un cambio de parámetro —"dale", "vamos", o directamente empieza a hablar del tema— tira con lo sugerido y empieza. Una sola ronda de preguntas: no vuelvas a preguntar lo mismo con otras palabras.

## Elección de formato — regla importante

**"Identificar el error" solo funciona bien con temas amplios.** Con un tema cerrado como *subjuntivo*, las opciones de respuesta resultan demasiado obvias — el error salta a la vista porque el usuario ya sabe qué está buscando. Con un tema amplio como *español de México* o *español B1*, obliga a pensar de verdad.

Cada tema del catálogo lleva su `amplitud`, así que esto no se juzga a ojo:

- `"amplitud": "cerrado"` (`FR.por-para`, `G.B2.condicionales-irreales`) → **completar**, **opciones** o **texto libre**.
- `"amplitud": "amplio"` (`FR.conectores`, `LX.B2.capa-abstracta`, `F.B2.argumentacion`) → **identificar el error** funciona muy bien.

Si el usuario pide "identificar el error" sobre un tema cerrado, hazlo igualmente pero avísale en una línea de que las respuestas pueden resultar obvias y ofrécele el formato alternativo.

Detalle de cada formato: `../../references/formatos.md`.

## Ritmo de entrega

Dos maneras de servir la misma tanda. **Por defecto, uno a uno.**

| Ritmo | Cómo va |
|---|---|
| **uno a uno** | Un solo ejercicio por mensaje. El usuario responde, corriges ese ítem entero, y solo entonces sale el siguiente. Es el modo por defecto: más conversación, feedback en caliente, y puedes ajustar la dificultad de lo que queda según cómo vaya respondiendo. |
| **tanda** | Los 8–10 ejercicios numerados de golpe. El usuario responde a su ritmo, de golpe o por partes; corriges cada respuesta según llega. Útil si quiere verlos todos, imprimirlos o resolverlos sin interrupciones. |

**Se pregunta al abrir**, junto con tema y formato, en el mismo mensaje y con su sugerencia — ver "Apertura: preguntar con sugerencia". Si el usuario ya lo ha dicho en su mensaje ("de una en una", "dámelos todos", "one at a time") no lo preguntes: dalo por confirmado y anúncialo.

Se puede cambiar a mitad de sesión: "dámelos todos ya", "mejor de una en una". Cámbialo sin ceremonia y sigue por donde ibas.

### En uno a uno

- **Diseña la tanda entera antes de servir el primer ítem.** Sigue habiendo 8–10 ejercicios con su reparto de dificultad y su cobertura del tema (ver "Perfil de nivel"); lo único que cambia es que se sirven de a uno. Sin plan previo, la sesión se convierte en ocho ítems sueltos del mismo subpunto.
- **Numera siempre: `3/8`.** El usuario tiene que saber por dónde va y cuánto queda.
- Un mensaje = un ejercicio. Nada de adelantar el siguiente "por si acaso".
- Corrige con el mismo detalle de siempre —regla, por qué falla lo suyo, abanico completo— y **cierra con el ejercicio siguiente en el mismo mensaje**, sin preámbulo. Feedback y siguiente ítem van juntos; no hagas esperar un turno extra.
- **Aprovecha lo que ves.** Si falla dos ítems seguidos por lo mismo, mete el siguiente en ese punto en vez de pasar al que tocaba. Si va sobrado, sube al ítem más duro del plan. Anuncia el cambio en media línea al hacerlo.
- El plan es una guía, no un contrato: puedes cortar en el 6 si el usuario ya lo tiene, o alargar si está enganchado. Dilo al cerrar.

## Cómo se ejecuta la sesión

0. **Antes de nada, mira si toca repaso.** Lee `$SPANISH_PRACTICE_DATA/aprendido.jsonl` — la carpeta de datos es `~/.spanish-practice` salvo que `SPANISH_PRACTICE_DATA` la mueva, que es lo que hace `~/.zshenv` en esta máquina para mandarla a iCloud Drive. Los scripts la resuelven solos; vive fuera del repo a propósito. Si existe y tiene líneas, aplica la selección de `../../references/repaso.md`: hay ~70 % de probabilidad de abrir con **2–3 ítems ya aprendidos** en forma de ejercicio, antes del tema del día. Si el fichero no existe o está vacío, pasa al paso 1 sin decir nada.
1. Si toca repaso: sirve esos 2–3 ítems, corrige, actualiza sus líneas en el fichero y **transiciona en una frase** al tema pedido. Nada de resúmenes largos — la apertura es un calentamiento, no la sesión. Si el usuario dice "hoy no" o "sin repaso", salta directo al paso 2.
2. Ejecuta `python3 estadisticas.py` y **pregunta** **tema**, **formato** y **ritmo** en un solo mensaje con la sugerencia que devuelva — ver "Apertura: preguntar con sugerencia". El nivel no se pregunta. Lo que el usuario ya haya dicho no se pregunta. Una sola ronda. En cuanto estén confirmados —ni antes— abre la sesión con el script, que es quien pone la fecha y el id:
   ```bash
   python3 abrir_sesion.py --tema-id FR.valores-de-se --formato completar --ritmo uno-a-uno --repaso-apertura no
   ```
   **Guarda el id que imprime**: hace falta en cada respuesta y al cerrar.
3. Diseña la tanda entera de ejercicios numerados. **No des las respuestas todavía.** Sírvela según el ritmo:
   - **uno a uno** (defecto) → solo el ejercicio `1/8` en este mensaje; el resto se queda en tu plan, sin enseñarlo.
   - **tanda** → los 8–10 numerados de golpe.
4. Espera a que el usuario responda. En tanda puede responder a todos de golpe o por partes; si responde de uno en uno, corrige ese ítem al momento y no esperes al resto.
5. Da feedback **ejercicio por ejercicio** — y en uno a uno, el ejercicio siguiente va en ese mismo mensaje, detrás del feedback:
   - ✅ / ❌ y la respuesta correcta.
   - **Por qué** es correcta — la regla, no solo la etiqueta.
   - **Por qué falla** lo que puso el usuario, si falló.
   - **Todas las demás formas gramaticales**, cada una con la lectura que la hace válida. Obligatorio, no opcional — ver "Regla del abanico completo".
   - **Y registra la respuesta con `registrar.py`, en ese mismo turno** — ver "Registro de respuestas". No lo dejes para el final.
6. Cierra con un resumen breve: qué domina, qué conviene repasar, y ofrece otra tanda (más difícil, mismo tema; o tema nuevo). Si en la sesión ha caído algún "ah, ahora lo veo", ofrece apuntarlo (skill `spanish-practice:recordar`). Cierra la sesión con `python3 cerrar_sesion.py --sesion <id>`: el recuento sale de lo registrado, no lo escribas a mano.

## Registro de respuestas — `respuestas.jsonl`

**Cada ejercicio corregido deja una línea.** Es el fondo de datos a largo plazo: de aquí salen todas las tasas de acierto y, con ellas, la sugerencia de tema. Sin esto, la insistencia por tema no tiene con qué decidir.

Llámalo **en el mismo turno en que corriges**, no al final. Si el usuario se va a mitad de sesión, lo respondido hasta ahí queda guardado igual.

```bash
cd /Users/theo/.dotfiles/agents/plugins/spanish-practice/scripts
python3 registrar.py --sesion 2026-08-04-1232 --n 3/8 \
  --tema-id G.B1.pronombres-atonos --subtema-id FR.valores-de-se \
  --formato completar --correcto no \
  --respuesta "se me olvidó las llaves" --esperada "se me olvidaron las llaves" \
  --tipo error --nota "concordancia con el sujeto pospuesto"
```

| campo | qué va |
|---|---|
| `--sesion` | El id que imprimió `abrir_sesion.py`. El script rechaza uno que no exista. |
| `--tema-id` | El id del tema de la sesión. |
| `--subtema-id` | **El punto que mide de verdad ese ejercicio**, normalmente un `FR.*`. Es lo que permite decir "el tema va bien pero el *se* accidental sigue fallando". Ponlo siempre que puedas. |
| `--correcto` | `si` / `no` / `parcial`. Un parcial vale media respuesta en las tasas. |
| `--respuesta` | Lo que puso el usuario, **literal**. No lo normalices ni lo arregles. |
| `--tipo` | Solo si falló: `error` (agramatical) o `preferencia` (gramatical pero poco idiomático). |
| `--nota` | La regla que se cayó, en una línea. |
| `--repaso` | Marca el ítem como parte del repaso de apertura: no cuenta para el tema del día. |

## Registro de sesiones — `sesiones.jsonl`

Una línea por sesión. **No la escribas a mano**: `abrir_sesion.py` la añade (con el id, la fecha y la hora del reloj del sistema, y el nivel de `config.json`) y `cerrar_sesion.py` le añade el `resultado` calculado desde `respuestas.jsonl`.

```json
{"id": "2026-08-04-1232", "fecha": "2026-08-04", "hora": "12:32", "tipo": "practica", "tema_id": "FR.valores-de-se", "tema": "Valores de se, incluido el se accidental con OI", "nivel_tema": "B1/B2", "formato": "completar", "nivel": "B1/B2", "ritmo": "uno-a-uno", "repaso_apertura": false, "resultado": {"ejercicios": 8, "aciertos": 5, "parciales": 1, "tasa": 0.625, "temas_flojos": ["FR.valores-de-se"]}}
```

`tipo` es `practica` aquí y `repaso` en la skill `spanish-practice:repaso`. Si el usuario se va sin cerrar, la línea se queda sin `resultado` y así se queda: una sesión a medias se ve como lo que fue, y no cuenta para consolidar. No la completes a ojo ni la borres.

## Scripts

Todos en `/Users/theo/.dotfiles/agents/plugins/spanish-practice/scripts`, sin dependencias, ejecutables con `python3`.

**Dónde está cada cosa**, que son dos sitios distintos a propósito:

| | dónde | por qué |
|---|---|---|
| Código, catálogo de temas, `config.defaults.json` | el plugin, en git | es contenido: se versiona y se revisa |
| `sesiones.jsonl`, `respuestas.jsonl`, `aprendido.jsonl`, `config.json` | la carpeta de datos, fuera del repo | es estado: crece en cada sesión, y el repo no se llena de commits de datos |

**La carpeta de datos es `~/.spanish-practice`**, salvo que `SPANISH_PRACTICE_DATA` diga otra cosa. En esta máquina sí lo dice: `~/.zshenv` la manda a iCloud Drive, para que el historial sobreviva a que muera el disco. Los scripts la resuelven solos en `comun.py`; tú no necesitas construir la ruta a mano — y si la variable se pierde, se paran antes que empezar un historial nuevo en paralelo. Detalle y montaje: `../../README.md`.

| script | para qué |
|---|---|
| `temas.py` | Consultar el catálogo: `--listar`, `--buscar`, `--bloque FR`. Texto del usuario → id. |
| `estadisticas.py` | Tasas por tema, subtema y formato + la sugerencia de apertura. `--json` para leerlo exacto. |
| `abrir_sesion.py` | Abre la sesión y devuelve su id. |
| `registrar.py` | Una llamada por ejercicio corregido. |
| `cerrar_sesion.py` | Calcula el `resultado` desde las respuestas y lo escribe. |

Los umbrales (`umbral_consolidacion`, `sesiones_para_consolidar`, `minimo_respuestas_sesion_valida`) y el perfil (`nivel`, `variedad`, `cantidad_ejercicios`, `ritmo_por_defecto`) salen de `config.defaults.json` del plugin, **pisados clave por clave** por `$SPANISH_PRACTICE_DATA/config.json`. Lo personal se toca en el segundo; el primero es el valor de fábrica. Si una sugerencia no cuadra, se cambia ahí — no improvisando al vuelo.

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
