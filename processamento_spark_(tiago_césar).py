# -*- coding: utf-8 -*-
"""Processamento -  Spark (Tiago César)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pFZqGaN0kH2iTYMSLCc4FjkSmoKuoWRR

# Atividade 5 - Processamentos de Dados (Spark)

Discente: Tiago César da Silva Lopes

Data: 21/09/23

## Link
https://www.who.int/data/gho/data/indicators/indicator-details/GHO/life-expectancy-at-birth-(years)


## Orientações

O dataset informa a expectativa de vida no nascimento e na idade de 60 anos em vários países. Note que quanto maior for o valor da expectativa de vida, melhor deve ser as condições de vida em um país.

## Instruções
Considerando a base de dados definida pelo aluno na Atividade 3, realize atividades de processamento, iniciada em sala (limpeza, seleção...) usando spark.

Pode usar o material compartilhado como exemplo, no entanto, deve ser aplicado a base de dados escolhida pelo aluno (individual).

## Instalação e exibição inicial do dataset
"""

!pip install pyspark

"""Iniciando uma sessão local e importando os dados:

"""

# Iniciar uma sessão local e importar dados
from pyspark.sql import SparkSession
sc = SparkSession.builder.master('local[*]').getOrCreate()

# carregar dados do meu computador
dados_spark = sc.read.csv("Life expectancy at birth (years).csv", header=True)

# Verificando o tipo de objeto criado
type(dados_spark)

# Verificando o dataset
dados_spark.show(5)

# Verificando o schema() deste spark dataframe
dados_spark.printSchema()

#Retornar o número de linhas
dados_spark.count()

"""## Criando um novo dataset com colunas selecionadas

O dataset original realmente precisa ser limpo e tratado. Dito isso, vamos gerar um novo dataset.
"""

#Selecionar colunas
dados_selecionados = dados_spark.select("Indicator","ParentLocation","Location","Period","Dim1","Value").show(truncate=False)

#Principais estatísticas
dados_spark.describe('Period').show(5)

dados_spark.describe('Value').show(5)

# Importar a função "col" para trabalhar com colunas
from pyspark.sql.functions import col

# Contar as ocorrências únicas e ordenar os resultados
dados_spark.groupBy("Indicator").count().orderBy(col("count").desc()).show(truncate=False)

#Ocorrências em uma variável
dados_spark.select("Indicator").distinct().show(truncate=False)

#importar sql: groupBy
from pyspark.sql import functions as F

dados_spark.groupBy("Indicator").agg(F.sum("Value")).show(truncate=False)

"""## Análise e extração de informações

### Qual o país com maior expectativa de vida?
"""

pais_maiorExpectativa2 = dados_spark.groupBy('ParentLocation').agg(F.count('Value').alias('count(Value)')).orderBy(F.desc('count(Value)')).show(truncate=False)

"""### Qual é maior: De acordo com os dados, a expectativa de vida no nascimento ou quando se tem 60 anos?"""

maior_expectativaVida = dados_spark.groupBy('Indicator').agg(F.sum('Value')).orderBy(F.sum('Value').desc()).show(truncate=False)

"""Logo, podemos concluir que a expectativa de vida nos países do mundo é maior no nascimento (154204.44) do que na população com 60 anos (41949.13).

154204.44 > 41949.13

### Qual é o gênero com maior expectativa de vida?
"""

genero_MaiorExpectativa = dados_spark.groupBy('Dim1').agg(F.sum('Value')).orderBy(F.sum('Value').desc()).show()

"""Para a surpresa de muitas pessoas, inclusive a minha, a expectativa de vida é maior para o gênero Feminino. De acordo com o dataset, a média de ambos os sexos é 65,398.98, enquanto que o feminino é 68,226.84 e o masculino é 62,527.75.

Logo, podemos concluir que as mulheres vivem mais do que os homens, mas isto eu deixo aberto para mais investigações.

 68,226.84 > 62,527.75

### Qual é o período que teve a maior expectativa de vida?
"""

periodo_maiorExpectativa = dados_spark.groupBy('Period').agg(F.sum('Value')).orderBy(F.sum('Value').desc()).show()

"""O ano com maior taxa de expectativa de vida foi o mais recente, 2019. Logo, podemos concluir que conforme os anos vão passando e as tecnologias evoluindo, a expectativa de vida também vai melhorando pelo mundo.

### Qual é a localização com maior expectativa de vida?
"""

location_maiorExpectativa = dados_spark.groupBy('Location').agg(F.sum('Value')).orderBy(F.sum('Value').desc()).show()

"""A lista acima exibe os locais com maiores expectativas de vida. Podemos notar nome de vários Locais conhecidos, como Japão, Canadá, Austrália, Espanha, Itália, Costa Rica entre outros. Note que neste dataset, o Japão registrou a maior taxa de expectativa de vida mundial.

### Qual a localização com a menor expectativa de vida?
"""

location_menorExpectativa = dados_spark.groupBy('Location').agg(F.sum('Value')).orderBy(F.sum('Value').asc()).show()

"""Acima é exibido os locais com as menores taxas de expectativas de vida, como o central da África, Haiti, Angola dentre outros. Isso tem fundamentação nos acontecimentos históricos e políticos que assolam essas localizações.

## Valores nulos
"""

#Dados faltantes
dados_spark.select([F.count(F.when(F.isnull(c), c)).alias(c) for c in dados_spark.columns]).show()

#substituir valores ausentes
dados_spark_sem_na = dados_spark.fillna({'Dim2 type':'Sem Resposta', 'Dim2':'Sem Resposta' , 'Dim2ValueCode':'Sem Resposta' , 'Dim3 type':'Sem Resposta' , 'Dim3':'Sem Resposta'
, 'Dim3ValueCode' : 'Sem Resposta' , 'DataSourceDimValueCode' : 'Sem Resposta' , 'DataSource' : 'Sem Resposta' , 'FactValueNumericPrefix' : 'Sem Resposta',
 'FactValueUoM' : 'Sem Resposta' , 'FactValueNumericLowPrefix' : 'Sem Resposta' , 'FactValueNumericLow' : 'Sem Resposta' , 'FactValueNumericHighPrefix' : 'Sem Resposta',
'FactValueTranslationID' : 'Sem Resposta' , 'FactComments' : 'Sem Resposta' , 'FactValueNumericHigh' : 'Sem Resposta'                                         })

dados_spark_sem_na.select([F.count(F.when(F.isnull(c), c)).alias(c) for c in dados_spark_sem_na.columns]).show()

"""Os valores nulos foram substituídos pelo texto 'Sem resposta', e assim não tem mais valor nulo no dataset."""

# Verificando o novo dataset
dados_spark_sem_na.show(5)

"""## Exclusão de colunas da base de dados"""

# Lista das colunas que vão ser excluídas
colunas_a_excluir = [
    'Dim2 type', 'Dim2', 'Dim2ValueCode',
    'Dim3 type', 'Dim3', 'Dim3ValueCode',
    'DataSourceDimValueCode', 'DataSource',
    'FactValueNumericPrefix', 'FactValueUoM',
    'FactValueNumericLowPrefix', 'FactValueNumericLow',
    'FactValueNumericHighPrefix', 'FactValueNumericHigh',
    'FactValueTranslationID', 'FactComments'
]

#Excluir colunas da base de dados
dados_spark = dados_spark.drop(*colunas_a_excluir)
dados_spark.show(5)

"""## Salvando o resultado e convertendo para pandas"""

# Salvar resultado
dados_spark_sem_na.write.csv("/content/dadosSpark")

# Spark para Pandas
dados_spark_sem_na_pd = dados_spark_sem_na.toPandas()

# Salvar resultado
dados_spark_sem_na_pd.to_csv("dados_pandas.csv")

dados_spark_sem_na_pd.head()