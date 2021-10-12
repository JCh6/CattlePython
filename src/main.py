### main.py

import pandas as pd
import matplotlib.pyplot as plt
from Log import Log
from usr.prefs import prefs
from CowManager import CowManager
from Statistics import Statistics

from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm

'''
Funcion para mostrar el menu 
'''
def menu():
    action = 1
    while action > 0:
        displayOptions()
        action = int(input())

        if action == 1:
            generate()
        elif action == 2:
            read()
        elif action == 3:
            predict()

'''
Funcion para mostrar las posibles opciones
'''
def displayOptions():
    print("-------- MENU --------")
    print("0. Salir")
    print("1. Generar .csv")
    print("2. Leer .xlsx")
    print("3. Modelo de regresión")
    print("----------------------")

'''
Funcion que realiza las siguientes acciones:
    - Cargar los archivos
    - Genera los mapa de calor
    - Guarda en un .csv la distacia recorrida por cada vaca
'''
def generate():
    cm = CowManager(prefs)
    cm.loadCows()
    cm.heatMap(True)
    distanceTraveled = cm.getDistanceTraveledPerDay()
    cm.genCSV(distanceTraveled, ["Vaca", "Distancia", "Dia"])

'''
Funcion que realiza las siguientes acciones:
    - Carga el archivo excel que contiene la produccion
    - Guarda un .xlsx con las metricas de la distancia, distancia total y produccion
    - Muestra en pantalla el diagrama de caja, el diagrama de barras y el histograma
'''
def read():
    # Leer archivo .xlsx
    s = Statistics(prefs)
    inputDataFrame = s.getDataFrame()
    columns = prefs["VARS"]

    # Crear excel con las metricas definidas
    s.createExcel({"Metrica": ["Varianza", "Desv. Estandar", "Coef. Variacion", "Kurtosis", "Asimetria"]})

    # Mostrar diagrama de caja
    boxplot = inputDataFrame.boxplot(column=columns)
    plt.show()

    # Mostrar diagrama de barras
    inputDataFrame.plot.bar(x="Dia", y="Producción ", rot=70, title="Producción de Leche x Vaca x Dia")
    plt.show(block=True)

     # Mostrar histograma
    hist = inputDataFrame.hist(bins=5)
    plt.show()

'''
Funcion que realiza las siguientes acciones:
    - Carga el archivo excel que contiene la produccion
    - Ejecuta el modelo analitico
'''
def predict():
    alpha = prefs["ALPHA"]
    x_var = prefs["X"]
    y_var = prefs["Y"]

    # Cargar archivo excel
    s = Statistics(prefs)
    datos = s.getDataFrame()

    # Grafico de dispersion (width x height)
    fig, ax = plt.subplots(figsize=(6, 3.84))

    datos.plot(
        x    = x_var,
        y    = y_var,
        c    = 'firebrick',
        kind = "scatter",
        ax   = ax
    )
    ax.set_title('Distribución de distancia recorrida y producción')

    fig.show()

    # Correlación lineal entre las dos variables
    corr_test = pearsonr(x=datos[x_var], y=datos[y_var])
    print("Coeficiente de correlación de Pearson: ", corr_test[0])
    print("P-value: ", corr_test[1])

    # El gráfico y el test de correlación muestran una relación lineal, de intensidad considerable (r = -0.866) y significativa (p-value <= 0.05). 
    # Tiene sentido intentar generar un modelo de regresión lineal con el objetivo de predecir la producción en función de la distancia recorrida de una vaca. 

    # A continuación se realiza la división de los datos en train y test
    # En este caso se intenta tomar un 80% de los datos para entrenamiento
    X = datos[[x_var]]
    y = datos[y_var]

    X_train, X_test, y_train, y_test = train_test_split(
                                            X.values.reshape(-1,1),
                                            y.values.reshape(-1,1),
                                            train_size   = 0.8,
                                            random_state = 1234,
                                            shuffle      = True
                                        )
    
    # Se realiza el modelo OLS (Mínimos cuadrados ordinarios) para regresión lineal
    # El valor de R-squared indica que el modelo es capaz de explicar el 74.1% de la variabilidad observada en la variable respuesta
    # Prob (F-statistic) <= 0.5) indica que sí hay evidencias de que la varianza explicada por el modelo es superior a la esperada por azar (varianza total).
    # El modelo generado es produccion = 26.7952 - 4.6532 * distancia
    X_train = sm.add_constant(X_train, prepend=True)
    modelo = sm.OLS(endog=y_train, exog=X_train,)
    modelo = modelo.fit()
    print(modelo.summary())

    # Intervalos de confianza para los coeficientes del modelo
    print("Intervalo de confianza para los coeficientes:")
    print(modelo.conf_int(alpha=alpha))

    # Predicciones con intervalo de confianza de (1 - alpha)
    predicciones = modelo.get_prediction(exog=X_train).summary_frame(alpha=alpha)
    predicciones['x'] = X_train[:, 1]
    predicciones['y'] = y_train
    predicciones = predicciones.sort_values('x')

    # Gráfico del modelo
    fig, ax = plt.subplots(figsize=(6, 3.84))

    ax.scatter(predicciones['x'], predicciones['y'], marker='o', color = "gray")
    ax.plot(predicciones['x'], predicciones["mean"], linestyle='-', label="OLS")
    ax.plot(predicciones['x'], predicciones["mean_ci_lower"], linestyle='--', color='red', label="95% CI")
    ax.plot(predicciones['x'], predicciones["mean_ci_upper"], linestyle='--', color='red')
    ax.fill_between(predicciones['x'], predicciones["mean_ci_lower"], predicciones["mean_ci_upper"], alpha=0.1)
    ax.legend()
    fig.show()

    # Error de test del modelo
    # El error de test del modelo es de 1.98. Las predicciones del modelo final se alejan en promedio 1.98 unidades del valor real. 
    X_test = sm.add_constant(X_test, prepend=True)
    predicciones = modelo.predict(exog = X_test)
    rmse = mean_squared_error(
            y_true  = y_test,
            y_pred  = predicciones,
            squared = False
        )
    print("")
    print(f"El error (rmse) de test es: {rmse}")


if __name__ == "__main__":
    log = Log()
    log.info("Log ready!")
    menu()