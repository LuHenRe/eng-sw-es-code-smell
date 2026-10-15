"""
Script cliente que demonstra o uso do Padrão Strategy para cálculo de frete.

O cliente é responsável por instanciar a estratégia desejada e injetá-la no
objeto Pedido através do método `set_estrategia()`. Em seguida, chama `calcular_frete()`
sem se preocupar com os detalhes internos de implementação do cálculo.
"""

from pedido import Pedido
from estrategia_frete import (
    FreteSedex,
    FretePac,
    FreteTransportadora,
    FreteMotoboy,
    FreteDrone,
)


def main():
    print("*" * 40)
    print("Executando Versão Refatorada (Strategy Pattern)")
    print("*" * 40)
    
    # Pedido 1 com peso de 2.5 kg
    pedido = Pedido(peso_kg=2.5)

    # 1. Frete via SEDEX (10.0 + 2.5 * 1.5 = 13.75)
    pedido.set_estrategia(FreteSedex())
    frete_sedex = pedido.calcular_frete()
    print(f"Valor do frete SEDEX: R$ {frete_sedex:.2f}")  

    # 2. Frete via PAC (5.0 + 2.5 * 1.0 = 7.50)
    pedido.set_estrategia(FretePac())
    frete_pac = pedido.calcular_frete()
    print(f"Valor do frete PAC: R$ {frete_pac:.2f}")  
    
    # 3. Frete via Transportadora (20.0 + 2.5 * 3.0 = 27.50)
    pedido.set_estrategia(FreteTransportadora())
    frete_transp = pedido.calcular_frete()
    print(f"Valor do frete TRANSPORTADORA: R$ {frete_transp:.2f}") 
    
    # 4. Frete via Motoboy (taxa fixa 15.00)
    pedido.set_estrategia(FreteMotoboy())
    frete_motoboy = pedido.calcular_frete()
    print(f"Valor do frete MOTOBOY: R$ {frete_motoboy:.2f}") 

    # 5. NOVO REQUISITO: Frete via Drone (taxa fixa 25.00) - Teste de Extensibilidade (OCP)
    pedido.set_estrategia(FreteDrone())
    frete_drone = pedido.calcular_frete()
    print(f"Valor do frete DRONE: R$ {frete_drone:.2f}")

    # Pedido 2 com peso de 10.0 kg via PAC (5.0 + 10.0 * 1.0 = 15.00)
    pedido2 = Pedido(peso_kg=10.0)
    pedido2.set_estrategia(FretePac())
    frete_pac_pedido2 = pedido2.calcular_frete()
    print(f"Valor do frete PAC (Pedido 10kg): R$ {frete_pac_pedido2:.2f}") 


# Ponto de entrada para execução
if __name__ == "__main__":
    main()