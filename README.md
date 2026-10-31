# numaris-web

Assets y código de la Home de numaris.com (Webflow), servidos vía jsDelivr.

```
frames/<vehiculo>/<desktop|mobile>/000.webp … 089.webp   (secuencias 3D, WebP transparente)
js/home.js                                              (interacciones de la Home)
```

URL de un frame:
`https://cdn.jsdelivr.net/gh/<usuario>/numaris-web@<tag>/frames/pesados/desktop/000.webp`

Vehículos: `pesados` (tractocamión), `distribucion` (caja refrigerada), `ligeros` (sedán).
Desktop 1600×900 · Mobile 800×450.

Usar siempre un tag fijo (`@v1.0.0`), nunca `@main`: los tags se cachean de forma permanente.
`_source/` (descargas originales de Drive) no se sube al repo (ver .gitignore).
