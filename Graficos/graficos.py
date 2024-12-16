import pandas as pd
import matplotlib.pyplot as plt

# Leer los datos de flights.csv
df = pd.read_csv('D:/Scraping/google_flights_scraper/flights.csv')

# Eliminar filas con valores nulos
df.dropna(inplace=True)

# Renombrar la columna 'airline' a 'destination'
df.rename(columns={'airline': 'destination'}, inplace=True)

# Convertir la columna 'price' a numérica (eliminar el símbolo de dólar y las comas)
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

# Mostrar todos los elementos únicos de la variable 'destination'
print(df['destination'].unique())
print(df.head())

# Diccionario de abreviaturas de ciudades
city_abbr = {
    'Los Angeles': 'LA',
    'San Francisco': 'SF',
    'Washington, D.C.': 'DC',
    'Edinburgh': 'EDI',
    'San Diego': 'SDIEGO',
    'New Orleans': 'NOLA',
    'Philadelphia': 'PHI',
    'Mexico City': 'MEX',
    'San Antonio': 'SANTONIO',
    'Fort Lauderdale': 'FTL',
    'Honolulu': 'HONO',
    'Ho Chi Minh City': 'HCMC',
    'Taipei City': 'TAI',
    
}

# Gráfico de barras de precios por destino
plt.figure(figsize=(15, 8))
price_plot = df.groupby('destination')['price'].mean().sort_values().plot(kind='bar')
plt.title('Precio promedio por destino')
plt.xlabel('Destino')
plt.ylabel('Precio promedio ($)')
price_plot.set_xticklabels([city_abbr.get(item.get_text(), item.get_text()) for item in price_plot.get_xticklabels()])
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig('precio_promedio_por_destino.png')
plt.show()
# Mostrar el precio promedio por cada destino
average_price_per_destination = df.groupby('destination')['price'].mean()
print('                                       ')
print(average_price_per_destination)

# Gráfico de barras de duración promedio por destino
df['duration'] = df['duration'].str.extract(r'(\d+)').astype(float)  # Extraer solo las horas de la duración
plt.figure(figsize=(15, 8))
duration_plot = df.groupby('destination')['duration'].mean().sort_values().plot(kind='bar')
plt.title('Duración promedio por destino')
plt.xlabel('Destino')
plt.ylabel('Duración promedio (horas)')
duration_plot.set_xticklabels([city_abbr.get(item.get_text(), item.get_text()) for item in duration_plot.get_xticklabels()])
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig('duracion_promedio_por_destino.png')
plt.show()
# Mostrar la duración promedio por cada destino
average_duration_per_destination = df.groupby('destination')['duration'].mean()
print('                                       ')
print(average_duration_per_destination)


# Gráfico de dispersión de precio vs duración
plt.figure(figsize=(15, 8))
plt.scatter(df['duration'], df['price'])
plt.title('Precio vs Duración')
plt.xlabel('Duración (horas)')
plt.ylabel('Precio ($)')
plt.tight_layout()
plt.savefig('precio_vs_duracion.png')
plt.show()