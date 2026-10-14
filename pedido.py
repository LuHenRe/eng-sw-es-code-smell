#Representa um pedido em um sistema de comércio eletrônico.
#Lógica de cálculo de frete (precisa ser refatorada).

class Pedido:    

    def __init__(self, peso_kg: float):
        self._peso_kg = peso_kg
    
    #Calcula o frete baseado no tipo de serviço.
    #Se um novo tipo de frete for adicionado, esta classe precisará ser modificada (viola o Princípio Aberto/Fechado).
    
    def calcular_frete(self, tipo_servico: str) -> float:
                
        print(f"Calculando frete para: {tipo_servico}")        
        servico = tipo_servico.upper()

        if servico == "SEDEX":
            return 10.0 + (self._peso_kg * 1.5)
        
        elif servico == "PAC":
            return 5.0 + (self._peso_kg * 1.0)
        
        elif servico == "TRANSPORTADORA":
            return 20.0 + (self._peso_kg * 3.0)
        
        elif servico == "MOTOBOY":
            return 15.0
        
        else:
            print(f"AVISO: Tipo de serviço '{tipo_servico}' desconhecido.")
            return 0.0

    # Propriedades (get's) para acesso seguro aos atributos
    @property
    def peso_kg(self) -> float:
        return self._peso_kg
