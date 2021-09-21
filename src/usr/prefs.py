### prefs.py

prefs = {}

# Archivos
prefs["FILES"]        = { "Cow1": "clean/Cow1.txt", "Cow2": "clean/Cow2.txt", "Cow3": "clean/Cow3.txt", "Cow4":"clean/Cow4.txt", "Cow5": "clean/Cow5.txt" }

# Columnas del archivo
prefs["COLUMNS"]      = { 0: "Lat", 1: "Lon", 2: "Time", 3: "Date" }

# Nombre de la columna latitud
prefs["LAT_KEY"]      = "Lat"

# Nombre de la columna longitud
prefs["LON_KEY"]      = "Lon"

# Nombre de la columna fecha
prefs["DATE_KEY"]     = "Date"

# Nombre del archivo de mapa de calor
prefs["MAP_FILENAME"] = "heatmap"

# Separador del archivo
prefs["SEPARATOR"]    = ","

# Coordenada central del mapa de calor
prefs["CENTER"]       = [4.76994, -74.23248]

# Zoom inicial del mapa de calor
prefs["ZOOM"]         = 20

# Ruta del archivo que contiene la produccion
prefs["INPUT"]        = "data/in/in.xlsx"

# Columnas a cargar del archivo de excel
prefs["COLS"]         = "A:E"

# Nombre de las columnas del archivo de excel
prefs["VARS"]         = ["Distancia", "Dist. Recorrida total", "Producción "]

# Nivel de significancia
prefs["ALPHA"]        = 0.05

# Variable independiente
prefs["X"]            = "Dist. Recorrida total"

# Variable de respueta
prefs["Y"]            = "Producción "
