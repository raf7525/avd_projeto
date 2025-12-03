# Documentação do Banco de Dados

Este documento descreve a estrutura do banco de dados PostgreSQL utilizado no projeto.

## Banco de Dados: `avd_wind_data`

## Tabela: `thermal_measurements`

Esta é a tabela principal que armazena todas as medições meteorológicas coletadas e os dados de conforto térmico calculados.

### Estrutura

| Coluna              | Tipo de Dado      | Chave     | Nulo? | Descrição                                                                 |
| ------------------- | ----------------- | --------- | ----- | ------------------------------------------------------------------------- |
| `id`                | `SERIAL`          | Primária  | Não   | Identificador único para cada registro de medição.                         |
| `timestamp`         | `TIMESTAMP`       |           | Não   | O carimbo de data e hora exato em que a medição foi registrada (em UTC).     |
| `temperature`       | `FLOAT`           |           | Não   | Temperatura do ar em graus Celsius (°C).                                   |
| `humidity`          | `FLOAT`           |           | Não   | Umidade relativa do ar em porcentagem (%).                                  |
| `wind_velocity`     | `FLOAT`           |           | Não   | Velocidade do vento em metros por segundo (m/s).                           |
| `pressure`          | `FLOAT`           |           | Não   | Pressão atmosférica ao nível da estação em milibares (mB).                 |
| `solar_radiation`   | `FLOAT`           |           | Não   | Radiação solar global em Watts por metro quadrado (W/m²).                    |
| `thermal_sensation` | `FLOAT`           |           | Sim   | O valor calculado da sensação térmica (pode ser Wind Chill ou Heat Index). |
| `comfort_zone`      | `VARCHAR(50)`     |           | Sim   | A classificação da zona de conforto (`Frio`, `Confortável`, `Quente`, etc.). |
| `created_at`        | `TIMESTAMP`       |           | Sim   | O carimbo de data e hora de quando o registro foi inserido no banco. Padrão: `CURRENT_TIMESTAMP`. |

### Exemplo de Consulta

```sql
SELECT * FROM thermal_measurements WHERE comfort_zone = 'Confortável' ORDER BY timestamp DESC LIMIT 10;
```
