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


class FreteSedex(EstrategiaFrete):
    """
    Estratégia concreta para cálculo de frete via SEDEX.
    
    Regra de negócio: Taxa fixa de R$ 10,00 acrescida de R$ 1,50 por kg do pedido.
    """

    def calcular(self, pedido: "Pedido") -> float:
        return 10.0 + (pedido.peso_kg * 1.5)


class FretePac(EstrategiaFrete):
    """
    Estratégia concreta para cálculo de frete via PAC.
    
    Regra de negócio: Taxa fixa de R$ 5,00 acrescida de R$ 1,00 por kg do pedido.
    """

    def calcular(self, pedido: "Pedido") -> float:
        return 5.0 + (pedido.peso_kg * 1.0)


class FreteTransportadora(EstrategiaFrete):
    """
    Estratégia concreta para cálculo de frete via Transportadora.
    
    Regra de negócio: Taxa fixa de R$ 20,00 acrescida de R$ 3,00 por kg do pedido.
    """

    def calcular(self, pedido: "Pedido") -> float:
        return 20.0 + (pedido.peso_kg * 3.0)


class FreteMotoboy(EstrategiaFrete):
    """
    Estratégia concreta para cálculo de frete via Motoboy (entrega expressa local).
    
    Regra de negócio: Taxa fixa de R$ 15,00 (independente do peso).
    """

    def calcular(self, pedido: "Pedido") -> float:
        return 15.0
