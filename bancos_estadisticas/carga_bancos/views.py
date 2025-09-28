from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from utils.parseos import _parse_fecha_yyyy_mm_dd, _fmt_ddmmaa
from django.conf import settings
from pathlib import Path

DATA_DIR = Path(settings.RAW_DATA_DIR)

# Mapeo: valor del <select> -> nombre de carpeta
BANK_FOLDERS = {
    "santander": "Santander",
    "bbva": "BBVA",
    "ing": "ING",
}



def cargar_fichero(request):
    context = {}

    if request.method == "POST":
        fichero = request.FILES.get("archivo")
        banco_key = request.POST.get("banco")          # santander | bbva | ing
        f_desde = request.POST.get("fecha_desde")      # YYYY-MM-DD
        f_hasta = request.POST.get("fecha_hasta")      # YYYY-MM-DD

        # --- Validaciones mínimas ---
        errores = []
        if not fichero:
            errores.append("Debes seleccionar un fichero.")
        if banco_key not in BANK_FOLDERS:
            errores.append("Debes seleccionar un banco válido.")
        if not f_desde or not f_hasta:
            errores.append("Debes indicar el rango de fechas.")
        else:
            try:
                d1 = _parse_fecha_yyyy_mm_dd(f_desde)
                d2 = _parse_fecha_yyyy_mm_dd(f_hasta)
                if d2 < d1:
                    errores.append("La fecha 'hasta' no puede ser anterior a 'desde'.")
            except ValueError:
                errores.append("Formato de fecha inválido.")

        if errores:
            context["errores"] = errores
            return render(request, "cargar_ficheros.html", context)

        # --- Construcción de ruta y nombre final ---
        carpeta = BANK_FOLDERS[banco_key]          # p.ej. "ING"
        destino = DATA_DIR / carpeta               # p.ej. /.../data/ING
        destino.mkdir(parents=True, exist_ok=True)

        # nombre base: <carpeta_en_minusculas>_<ddmmaa>_<ddmmaa>
        base_name = f"{carpeta.lower()}_{_fmt_ddmmaa(d1)}_{_fmt_ddmmaa(d2)}"
        ext = Path(fichero.name).suffix  # conserva extensión original (.pdf, .xlsx, etc.)
        if not ext:
            ext = ""

        # Evitar colisión: si existe, añade _1, _2, ...
        final_name = base_name + ext
        i = 1
        while (destino / final_name).exists():
            final_name = f"{base_name}_{i}{ext}"
            i += 1

        # Guardar
        fs = FileSystemStorage(location=destino)   # fuera de MEDIA_ROOT
        fs.save(final_name, fichero)

        context.update({
            "ok": True,
            "banco": carpeta,
            "filename": final_name,
            "saved_path": destino / final_name,
            "rango": f"{d1.strftime('%d/%m/%Y')} - {d2.strftime('%d/%m/%Y')}",
        })

    return render(request, "cargar_ficheros.html", context)





