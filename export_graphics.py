import pandas as pd
import plotly.express as px

s10 = pd.read_excel("exportaciones_coffee.xlsx", sheet_name=9)
s10['total_kg'] = s10['Sacos de 70 kg. equivalente real Exportados'] * 70
s10['fecha'] = pd.to_datetime(s10['Año'].astype(str) + '-' + s10['Mes'].astype(str) + '-01')
s10.rename(columns={'Sacos de 70 kg. equivalente real Exportados': 'sacos_70',
                   'Sacos de 60 Kg. Exportados': 'sacos_60','Valor Factura (USD)*': 'valor_usd',
                   'Año': 'año',
                   }, inplace=True)

paises = s10['País destino'].unique()
for pais_nombre in paises:
    # Filtrar el DataFrame por país específico
    pais = s10[s10['País destino'] == pais_nombre]
    
    # Calcular el total de años y meses únicos en el país filtrado
    total_años = pais['año'].nunique()
    total_meses = pais['Mes'].nunique()
    
    # Filtrar exportadores con registros en todos los años y meses
    exportadores_completos = pais.groupby('Nombre exportador').filter(
        lambda x: x['año'].nunique() == total_años and x['Mes'].nunique() == total_meses
    )
    if exportadores_completos.empty:
        print(f"No hay exportadores completos para el país: {pais_nombre}")
        continue
    # Ordenar por fecha y resetear el índice
    exportadores_completos = exportadores_completos.sort_values(by='fecha').reset_index(drop=True)
    
    # Crear la gráfica
    fig = px.line(
        exportadores_completos, 
        x='fecha', 
        y='total_kg', 
        color='Nombre exportador', 
        title=f'Exportaciones con País destino {pais_nombre}', 
        width=800,
        height=400
    )
    fig.show()
    # Guardar la gráfica como imagen
    fig.write_image(f'{pais_nombre}.png')