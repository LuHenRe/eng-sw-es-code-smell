# Refatoração de Code Smell - Princípio Aberto/Fechado (OCP) com Padrão Strategy

Atividade prática baseada na identificação e refatoração de um **Code Smell** que viola o **Princípio Aberto/Fechado (OCP - Open/Closed Principle)**, aplicando o **Padrão de Projeto Strategy**.

---

## 1. O Problema (Antes da Refatoração)

No código inicial, a classe `Pedido` no arquivo `pedido.py` continha um método `calcular_frete(tipo_servico: str)` estruturado com múltiplos condicionais (`if-elif-else`):

```python
if servico == "SEDEX":
    return 10.0 + (self._peso_kg * 1.5)
elif servico == "PAC":
    return 5.0 + (self._peso_kg * 1.0)
elif servico == "TRANSPORTADORA":
    return 20.0 + (self._peso_kg * 3.0)
elif servico == "MOTOBOY":
    return 15.0
```

### Por que isso viola o Princípio Aberto/Fechado (OCP)?
- O **OCP** determina que classes devem estar **abertas para extensão**, mas **fechadas para modificação**.
- Sempre que a empresa decidisse adicionar uma nova modalidade de entrega (ex: `DRONE` ou `RETIRADA_LOCAL`), a classe `Pedido` — que já estava testada e funcionando — precisaria ser **reaberta e modificada**.
- Esse acoplamento gera riscos de introduzir novos bugs (*efeitos colaterais*), aumenta a complexidade ciclomática e viola a coesão da classe.

---

## 2. A Solução (Padrão de Projeto Strategy)

O padrão **Strategy** permite definir uma família de algoritmos, encapsular cada um deles em classes separadas e torná-los intercambiáveis. O algoritmo pode variar independentemente dos clientes que o utilizam.

### Estrutura dos Componentes:
1. **Interface/Estratégia Abstrata (`EstrategiaFrete`)**:
   - Define a interface comum `calcular(self, pedido) -> float`.
   - Localizada em `estrategia_frete.py`.
2. **Estratégias Concretas**:
   - `FreteSedex`: R$ 10,00 fixo + R$ 1,50/kg.
   - `FretePac`: R$ 5,00 fixo + R$ 1,00/kg.
   - `FreteTransportadora`: R$ 20,00 fixo + R$ 3,00/kg.
   - `FreteMotoboy`: R$ 15,00 fixo.
   - `FreteDrone`: R$ 25,00 fixo (novo requisito implementado no Passo 5).
3. **Contexto (`Pedido`)**:
   - Mantém uma referência para a estratégia selecionada via atributo privado `_estrategia`.
   - Expõe o método setter `set_estrategia(self, estrategia: EstrategiaFrete)`.
   - O método `calcular_frete()` agora apenas delega a execução: `self._estrategia.calcular(self)`.
4. **Cliente (`teste-frete.py`)**:
   - Cria o pedido, injeta a estratégia de frete desejada e dispara o cálculo.

---

## 3. Passo a Passo Realizado

- **Passo 1:** Criada a classe abstrata `EstrategiaFrete` em `estrategia_frete.py` usando `abc.ABC` e `@abstractmethod`.
- **Passo 2:** Criadas as estratégias concretas (`FreteSedex`, `FretePac`, `FreteTransportadora`, `FreteMotoboy`).
- **Passo 3:** Refatorada a classe `Pedido` em `pedido.py` para atuar como Contexto, removendo condicionais e delegando o cálculo via `set_estrategia` e `calcular_frete()`.
- **Passo 4:** Atualizado o cliente `teste-frete.py` para injetar as instâncias de estratégia no pedido.
- **Passo 5 (Teste de Extensibilidade):** Adicionada a classe `FreteDrone` (R$ 25,00 fixos). O novo tipo de frete foi incorporado **sem alterar nenhuma linha da classe `Pedido`**, comprovando na prática o Princípio Aberto/Fechado.
- **Passo 6 (Documentação e Explicação):** Adicionadas docstrings explicativas em todos os módulos e este README detalhado.

---

## 4. Como Executar

Para rodar os testes e verificar o funcionamento:

```bash
python teste-frete.py
```

### Saída esperada:
```text
****************************************
Executando Versão Refatorada (Strategy Pattern)
****************************************
Valor do frete SEDEX: R$ 13.75
Valor do frete PAC: R$ 7.50
Valor do frete TRANSPORTADORA: R$ 27.50
Valor do frete MOTOBOY: R$ 15.00
Valor do frete DRONE: R$ 25.00
Valor do frete PAC (Pedido 10kg): R$ 15.00
```
