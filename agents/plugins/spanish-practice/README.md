# spanish-practice

Plugin de práctica de español: ejercicios por tema, registro de cada respuesta y
repaso espaciado. Tres skills (`spanish-practice`, `repaso`, `recordar`) y cinco
scripts que hacen el trabajo determinista para que el modelo no lo improvise.

## Código aquí, datos fuera

| | dónde | por qué |
|---|---|---|
| `skills/`, `references/`, `scripts/`, `config.defaults.json` | este repo | es contenido: se versiona y se revisa |
| `sesiones.jsonl`, `respuestas.jsonl`, `aprendido.jsonl`, `config.json` | **fuera del repo** — ver abajo | es estado: crece en cada sesión |

Meter el historial en git obligaría a commitear después de cada sesión o a acumular
datos rancios en el repo. Ninguna de las dos cosa merece la pena.

## Dónde van los datos

Por defecto, **`~/.spanish-practice`**. Ruta fija, sin depender de macOS ni de ningún
servicio: `Path.home() / ".spanish-practice"` en `scripts/comun.py`. Los cinco scripts
importan de ahí, así que no hay nada que mantener sincronizado entre ellos.

Ese sitio por defecto **no sincroniza nada**, así que un disco muerto se lleva el
historial. Para evitarlo, apunta `SPANISH_PRACTICE_DATA` a una carpeta que sí
sincronice. En esta máquina, en `~/.zshenv`:

```sh
export SPANISH_PRACTICE_DATA="$HOME/Library/Mobile Documents/com~apple~CloudDocs/spanish-practice"
```

Va en `~/.zshenv`, **no** en `.zshrc`: `.zshrc` solo lo leen los shells interactivos
y Claude Code lanza uno no interactivo, así que los scripts no verían la variable.

Dos avisos sobre el destino, aprendidos por las malas en esta máquina:

- `~/Documents` **no** sirve aquí: la sincronización de Escritorio y Documentos de
  iCloud está apagada (`defaults read com.apple.finder FXICloudDriveDocuments` → `0`),
  así que esa carpeta es puramente local aunque lo parezca. Tiene que ser iCloud Drive
  de verdad, dentro de `~/Library/Mobile Documents/com~apple~CloudDocs`.
- Comprueba el destino antes de fiarte de él. Una ruta que *parece* sincronizada pero
  no lo está es el fallo que no se descubre hasta que se pierde el disco.

### Red de seguridad

Si la variable no está puesta, el sitio por defecto está vacío, y hay historial en una
carpeta sincronizada conocida, los scripts **se paran y lo dicen** en vez de empezar un
historial nuevo en paralelo (`verificar_datos()` en `scripts/comun.py`). Partir el
historial en dos es peor que fallar.

## Config en dos capas

`config.defaults.json` (aquí, versionado) marca los valores de fábrica. `config.json`
(en la carpeta de datos, personal) los pisa **clave por clave**, así que un umbral nuevo
llega sin tener que tocar el fichero personal, y lo personal no acaba en git.

| clave | qué es |
|---|---|
| `nivel` | Perfil del usuario. **No se pregunta en la sesión**, se lee de aquí. |
| `variedad` | Variedad de español por defecto. |
| `cantidad_ejercicios` | Rango de ejercicios por tanda. |
| `ritmo_por_defecto` | `uno-a-uno` o `tanda`, cuando no hay historial. |
| `umbral_consolidacion` | Tasa a partir de la cual un tema cuenta como bueno (0,8). |
| `sesiones_para_consolidar` | Cuántas sesiones seguidas hay que pasar el umbral (2). |
| `minimo_respuestas_sesion_valida` | Por debajo de esto, la sesión no cuenta como evidencia (5). |

## Scripts

Sin dependencias, `python3` a secas.

| script | para qué |
|---|---|
| `temas.py` | Catálogo oficial de temas: `--listar`, `--buscar`, `--bloque FR`. Texto libre → id. |
| `estadisticas.py` | Tasas por tema, subtema y formato + la sugerencia de apertura. `--json` para leerlo exacto. |
| `abrir_sesion.py` | Abre la sesión, pone id y fecha del reloj del sistema, devuelve el id. |
| `registrar.py` | Una llamada por ejercicio corregido. |
| `cerrar_sesion.py` | Calcula el `resultado` desde las respuestas registradas. |

Para probar sin tocar los datos de verdad, las dos rutas se pueden mover:

```sh
SPANISH_PRACTICE_DIR=/tmp/copia SPANISH_PRACTICE_DATA=/tmp/datos python3 estadisticas.py
```

## Temas con id

Los temas no son texto libre: están en `references/temas.json`, 103 entradas derivadas
del inventario del **Plan curricular del Instituto Cervantes** que documenta
`references/niveles-cefr.md`. Bloques `G.*` (gramática), `F.*` (funciones),
`LX.*` (léxico) y `FR.*` (los 20 puntos de la frontera B1→B2). Sesiones, respuestas y
estadísticas van todas por id, y los scripts rechazan uno que no esté en el catálogo.
