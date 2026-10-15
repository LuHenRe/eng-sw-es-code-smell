from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedido import Pedido


class EstrategiaFrete(ABC):
    """
    Interface / Classe Abstrata que define o contrato para todas as estratégias de frete (Padrão Strategy).
    
    Qualquer nova forma de cálculo de frete deve herdar desta classe e implementar
    o método `calcular`, garantindo que a classe `Pedido` dependa apenas desta abstração
    e não de implementações concretas (Princípio da Inversão de Dependência e Princípio Aberto/Fechado).
    """

    @abstractmethod
    def calcular(self, pedido: "Pedido") -> float:
        """
        Calcula o valor do frete com base nas informações do pedido (ex: peso).

        :param pedido: Instância do pedido que contém os dados necessários para o cálculo.
        :return: Valor total do frete em reais (float).
        """
        pass
