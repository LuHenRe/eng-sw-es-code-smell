from pedido import Pedido

def main():
    print("*" * 30)
    print("Executando Versão Inicial")
    print("*" * 30)
    
    pedido = Pedido(peso_kg=2.5)

    frete_sedex = pedido.calcular_frete("SEDEX")
    print(f"Valor do frete SEDEX: R$ {frete_sedex:.2f}")  

    frete_pac = pedido.calcular_frete("PAC")
    print(f"Valor do frete PAC: R$ {frete_pac:.2f}")  
    
    frete_transp = pedido.calcular_frete("TRANSPORTADORA")
    print(f"Valor do frete TRANSPORTADORA: R$ {frete_transp:.2f}") 
    
    frete_motoboy = pedido.calcular_frete("MOTOBOY")
    print(f"Valor do frete MOTOBOY: R$ {frete_motoboy:.2f}") 

    pedido2 = Pedido(peso_kg=10.0)
    frete_pac = pedido.calcular_frete("PAC")
    print(f"Valor do frete PAC: R$ {frete_pac:.2f}") 

#ponto de entrada para execução
if __name__ == "__main__":
    main()