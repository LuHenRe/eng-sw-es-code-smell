from typing import Optional
from estrategia_frete import EstrategiaFrete


class Pedido:
    """
    Representa o Contexto no Padrão de Projeto Strategy.
    
    A classe Pedido armazena os dados do pedido (como peso_kg) e delega
    o cálculo do frete para um objeto que implementa a interface EstrategiaFrete.
    Dessa forma, a classe Pedido está em conformidade com o Princípio Aberto/Fechado (OCP),
    pois novas formas de frete podem ser introduzidas sem que esta classe precise ser alterada.
    """

    def __init__(self, peso_kg: float, estrategia: Optional[EstrategiaFrete] = None):
        """
        Inicializa o pedido com seu peso e opcionalmente uma estratégia de frete.

        :param peso_kg: Peso do pedido em quilogramas.
        :param estrategia: Instância de uma classe que implementa EstrategiaFrete (opcional).
        """
        self._peso_kg = peso_kg
        self._estrategia = estrategia

    def set_estrategia(self, estrategia: EstrategiaFrete) -> None:
        """
        Define ou altera a estratégia de frete em tempo de execução (Setter público).

        :param estrategia: Instância de EstrategiaFrete a ser aplicada.
        """
        self._estrategia = estrategia

    def calcular_frete(self) -> float:
        """
        Delega o cálculo do frete para a estratégia configurada.
        
        Não há mais lógica condicional (if/elif/switch). O pedido simplesmente
        solicita à estratégia que calcule o valor, passando a si próprio (self)
        para que a estratégia possa acessar as informações necessárias (como peso_kg).

        :return: Valor do frete calculado pela estratégia em reais (float).
        :raises ValueError: Caso nenhuma estratégia tenha sido definida antes do cálculo.
        """
        if self._estrategia is None:
            raise ValueError("Estratégia de frete não definida. Utilize set_estrategia() antes de calcular.")
        
        return self._estrategia.calcular(self)

    # Suporte a métodos camelCase conforme mencionado no enunciado (calcularFrete)
    setEstrategia = set_estrategia
    calcularFrete = calcular_frete

    @property
    def peso_kg(self) -> float:
        """Propriedade para acesso seguro ao peso do pedido."""
        return self._peso_kg

    @property
    def estrategia(self) -> Optional[EstrategiaFrete]:
        """Propriedade para leitura da estratégia atual."""
        return self._estrategia

    @estrategia.setter
    def estrategia(self, estrategia: EstrategiaFrete) -> None:
        """Setter via property para definir a estratégia."""
        self.set_estrategia(estrategia)
