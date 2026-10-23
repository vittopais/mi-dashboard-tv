# Panel personal para la tele

Panel web en español para una Sony con Android TV. Incluye reloj y fecha de Argentina, clima local, pronóstico de lluvia en nueve zonas cercanas, agenda y tres titulares en cada una de cinco secciones.

## Publicarlo gratis en GitHub Pages

El sitio está listo para subirse a un repositorio de GitHub. Para publicarlo:

1. Creá un repositorio llamado `mi-dashboard-tv` y subí **todo el contenido de esta carpeta** a la carpeta principal del repositorio, incluidas las carpetas ocultas `.github` y `scripts`.
2. En el repositorio, abrí **Settings → Pages** y en **Build and deployment** elegí **GitHub Actions**.
3. La publicación automática se ejecutará al subir los archivos. También actualizará las noticias aproximadamente cada 15 minutos.
4. GitHub mostrará una dirección similar a `https://tu-usuario.github.io/mi-dashboard-tv/`.

El repositorio debe ser público para usar GitHub Pages gratis. El panel no sube la agenda ni guarda credenciales. El actualizador trae los titulares desde Google News en el servidor de GitHub; así evita el bloqueo del convertidor RSS que impedía ver las noticias. GitHub puede retrasar ocasionalmente una ejecución programada.

## Abrirlo en la Sony

1. Conectá la tele a Internet y abrí Play Store.
2. Instalá **TV Bro** si aparece disponible para tu modelo. Es un navegador para Android TV que se maneja con el control remoto.
3. Escribí la dirección de GitHub Pages, usá **Pantalla completa** y guardala como favorito.

La página intenta mantener la pantalla activa si el navegador de la tele admite esa función. Sony puede activar su protector de pantalla o el apagado por inactividad según el modelo y los ajustes de energía. Revisá los ajustes de **Protector de pantalla** y **Ahorro de energía** de la tele. En pantallas OLED, dejá activadas sus protecciones contra retención.

## Qué se actualiza y qué se guarda

- El reloj y la fecha se actualizan en pantalla. Clima y lluvia por zonas se consultan cada 10 minutos; los titulares se regeneran aproximadamente cada 15 minutos.
- La cuadrícula muestra nueve zonas alrededor de la ubicación elegida. Alterna automáticamente cada ocho segundos entre la hora actual y las dos siguientes; en cada zona indica la probabilidad y los milímetros previstos para esa hora. Es pronóstico por zona, no una imagen de radar en movimiento.
- El clima usa Open-Meteo. Las noticias son titulares de Google News y cada tarjeta abre la nota original.
- La ubicación inicial es Buenos Aires. Se puede cambiar buscando una ciudad o autorizando la ubicación del navegador. Si elegís la ubicación actual, las coordenadas se envían a Open-Meteo para el pronóstico; la ubicación queda guardada solo en ese navegador.
- La agenda se guarda únicamente en el almacenamiento local del navegador de la tele. No se sincroniza con otros dispositivos ni se sube a GitHub.
