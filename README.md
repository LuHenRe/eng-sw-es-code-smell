Este projeto simples de cálculo de frete contém um "Code Smell" que viola um princípio de aberto/fechado.

1. O Problema

O arquivo `pedido.py` contém uma classe `Pedido` com um método `calcular_frete()`. Este método funciona, como você pode ver executando `teste_frete.py`.

No entanto, ele viola o Princípio Aberto/Fechado. O que acontece se precisarmos adicionar um novo frete "DRONE" (taxa fixa de R$ 25)? Teremos que modificar a classe `Pedido`, adicionando outro `elif`.

2. Tarefa - Padrão Strategy)

Sua tarefa é refatorar este código usando o **Padrão Strategy**.

1.  Crie a "Abstração: Crie uma classe Abstrata (usando `abc.ABC` e `@abstractmethod`) chamada `EstrategiaFrete`. Ela deve ter um método `calcular(self, pedido)`.
2.  Crie as "Concretas: Crie classes concretas que herdam de `EstrategiaFrete` para cada lógica: `FreteSedex`, `FretePac`, `FreteTransportadora`, `FreteMotoboy`. Mova a lógica do `if-elif` para o método `calcular` de cada classe.
3.  Refatore o "Contexto": Modifique a classe `Pedido` (o "Contexto").
    * Remova o método `calcular_frete(self, tipo_servico)`.
    * Adicione um atributo `estrategia` (ex: `self.estrategia: EstrategiaFrete`).
    * Adicione um método `set_estrategia(self, estrategia)`.
    * Crie um novo método `calcular_frete(self)` que delega a chamada: `return self.estrategia.calcular(self)`.
4.  Atualize o `teste_frete.py`: Mude o script de teste para:
    * Definir a estratégia no pedido: `pedido.set_estrategia(FreteSedex())`
    * Chamar o novo método: `pedido.calcular_frete()`
5.  Adicione o frete "DRONE" (taxa fixa de R$ 25). Você conseguiu fazer isso sem tocar na classe `Pedido`? (Você só deve ter criado uma *nova* classe `FreteDrone`).
