#https://www.youtube.com/watch?v=Av7dbpKVXYU

#-------- Librerias -------------
import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

#-------- Ingesta de datos -------
df = pl.read_csv("data/WorldCupMatches.csv")
df
#Ver las primeras observaciones
df.head()
#tipo de datos
df.describe()

#nombre columnas
df.columns

#--------- Limpieza de datos ---------
#cambio de los nombres de las columnas

df = df.rename({'Home Team Name' : 'HTN',
                'Home Team Goals': 'HTG',
                'Away Team Goals': 'ATG',
                'Away Team Name': 'ATN',
                'Win conditions': 'WC',
                'Half-time Home Goals':'HTHG',
                'Half-time Away Goals':'HTAG',
                'Home Team Initials':'HTI',
                'Away Team Initials':'ATI'
                })

# df = df.rename({col: col.replace(" ", "_").replace("(", "").replace(")", "").lower() for col in df.columns})

#cant. elementos nulos por columnas:
nulos_df = df.null_count()
nulos_df

#eliminando valores nulos
df_clean = df.drop_nulls()
df_clean

#eliminando la columna WC (no es provechosa)
df_clean = df_clean.drop("WC")

#----------- Filtrado de datos -------------
df_clean.filter(pl.col("HTG")>=8)

df_clean.filter(pl.col("HTG")+ pl.col("ATG") >=10)


#---------- Group_by ------------
#para sacar los arbitros principales, ordenando por año
df_clean.group_by("Year", maintain_order= True).agg(
    pl.col("Referee").unique().count().alias("count")
)

df_clean.group_by("Year", maintain_order= True).agg(
    pl.col("HTN").count().alias("count")
)

#Goles que se hicieron en el primer tiempo
df_clean.group_by("Year",maintain_order=True).agg(
    pl.col("HTHG").sum().alias("Goles de HT equipo local"),
    pl.col("HTAG").sum().alias("Goles de HT equipo visitante")
)


#ciudad donde más partidos se han jugado. 