# Mi casa · Panel para la tele

El panel está publicado gratis en GitHub Pages:

**https://vittopais.github.io/mi-dashboard-tv/**

El sitio está abierto al rastreo de buscadores y publica un sitemap. Que aparezca en los resultados depende de Google: rastrear e indexar puede tardar y no se garantiza de inmediato.

Incluye reloj y fecha de Argentina, clima local y pronóstico de cinco días, la lista de tareas “Día” de Notion y titulares en seis secciones: Argentina, Mundo, Economía, Ciencia, Tecnología e IA.

## Abrirlo en la Sony

1. Conectá la tele a Internet y abrí el navegador que tenga. Si no aparece uno, entrá a **Apps → Google Play Store**, buscá **TV Bro** e instalalo si figura compatible con tu tele.
2. Escribí **vittopais.github.io/mi-dashboard-tv/** en la barra de direcciones. No hace falta buscarlo en Google.
3. Cuando cargue, elegí **Pantalla completa** arriba a la derecha y guardá la dirección como favorito para abrirla después con el control remoto.

El sitio ya está alojado en GitHub Pages: queda disponible en Internet aunque tu computadora esté apagada. Solo necesitás que la tele tenga conexión a Internet. No hace falta usar la Flow Box; si preferís usarla, abrí allí el navegador y probá la misma dirección.

## Cómo se actualiza

- La hora y la fecha se mantienen al día. El clima y los titulares se actualizan automáticamente. La página revisa la lista de Notion cada minuto; GitHub sincroniza y publica cambios cada cinco minutos, aunque puede demorarse un poco más.
- La ubicación inicial es Buenos Aires. Se cambia con **Cambiar ubicación** o eligiendo la ubicación del navegador. La selección se guarda solo en ese navegador.
- La tarjeta “Mi día” reemplaza la agenda y muestra la lista de Notion en modo de lectura. Los cambios que tildes desde el celular aparecerán después de la próxima sincronización.

## Activar la sincronización de Notion

La web es pública, así que el contenido de “Día” que aparece en ella también será visible para cualquiera que conozca el enlace. Para conectar la lista, se necesita crear una integración de Notion con permiso de lectura, compartir únicamente esa página con la integración y guardar su clave en GitHub como secreto `NOTION_TOKEN` (Settings → Secrets and variables → Actions). No copies la clave en el código ni en un mensaje. Hasta que se configure, el sitio sigue funcionando y la tarjeta indica que falta activar la conexión.

## Para mantenerlo en pantalla

El panel pide mantener la pantalla activa cuando el navegador lo permite, pero la configuración de la tele tiene prioridad. En la Sony, abrí **Ajustes → Sistema → Alimentación y energía** (o **Preferencias del dispositivo → Energía**) y desactivá las opciones de apagado por inactividad. Revisá también que **Temporizador de apagado** esté desactivado. Los nombres exactos cambian según el modelo.

El protector de pantalla también depende del modelo: si la tele permite desactivarlo y el panel es LED/LCD, podés hacerlo para que el dashboard quede visible. Si es OLED, dejá activadas las protecciones de pantalla del fabricante; Sony recomienda el protector para reducir el riesgo de retención de imagen. La tele puede oscurecer o cubrir el panel por decisión del sistema aunque el sitio siga abierto.
