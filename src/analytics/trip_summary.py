from pyspark.sql import DataFrame


class TripSummary:

    def build(
        self,
        travels: DataFrame,
        drivers: DataFrame,
        vehicles: DataFrame
    ) -> DataFrame:

        return (
            travels
            .join(
                drivers.select(
                    "motorista_id",
                    "nome"
                ),
                "motorista_id",
                "left"
            )
            .join(
                vehicles.select(
                    "veiculo_id",
                    "placa",
                    "marca",
                    "modelo"
                ),
                "veiculo_id",
                "left"
            )
            .select(
                "viagem_id",
                "motorista_id",
                "nome",
                "veiculo_id",
                "placa",
                "marca",
                "modelo",
                "geocerca_origem_id",
                "geocerca_destino_id",
                "status",
                "data_inicio",
                "data_fim_real",
                "peso_carga_kg",
                "distancia_km"
            )
        )