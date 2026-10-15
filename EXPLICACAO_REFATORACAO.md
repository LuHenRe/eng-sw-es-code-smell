# Explicação Detalhada da Refatoração - Padrão Strategy e Princípio Aberto/Fechado (OCP)

Este documento apresenta a análise completa, a justificativa teórica e as decisões de design adotadas durante a refatoração do sistema de cálculo de frete de e-commerce, com base nos conceitos da Aula 8 de Engenharia de Software.

---

## 1. O Problema Original e a Identificação do Code Smell

### Código Original (Antes da Refatoração)
No arquivo `pedido.py`, o cálculo de frete era realizado diretamente dentro da classe `Pedido` através de uma cadeia condicional (`if-elif-else`) que dependia do nome textual do serviço:

```python
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
```

### Code Smell Identificado
* **Conditional Complexity / Long Method (Switch Statements):** Múltiplos desvios condicionais para selecionar diferentes variações de um mesmo algoritmo.
* **Alto Acoplamento:** A classe `Pedido` concentrava regras de negócio de frete que não pertencem ao modelo de dados do pedido.
* **Fragilidade por Tipagem Fraca (Strings):** Passar strings como `"SEDEX"` ou `"PAC"` é suscetível a erros de digitação em tempo de execução que não são pegos pelo interpretador.

### Violação do Princípio Aberto/Fechado (OCP)
O **Princípio Aberto/Fechado (Open/Closed Principle - OCP)**, segundo componente do acrônimo **SOLID**, estabelece que:

> *"Entidades de software (classes, módulos, funções) devem estar abertas para extensão, mas fechadas para modificação."*

* **Aberto para extensão:** O comportamento do sistema deve ser capaz de crescer e aceitar novas regras.
* **Fechado para modificação:** O código existente, já testado e em produção, **não deve ser alterado** a cada nova funcionalidade.

No código original, caso o gerente de produto solicitasse a inclusão de modalidades como **"DRONE"** (taxa fixa de R$ 25,00) ou **"RETIRADA_LOCAL"** (custo zero), o desenvolvedor seria **forçado a abrir a classe `Pedido`** e adicionar novos blocos `elif`. Isso violava diretamente o OCP, criando o risco de quebrar cálculos já validados e aumentando a complexidade de manutenção.

---

## 2. A Solução com o Padrão de Projeto Strategy

O padrão de projeto comportamental **Strategy** (GoF) foi aplicado para extrair a família de algoritmos de frete de dentro de `Pedido` e colocá-los em classes separadas e intercambiáveis.

### Arquitetura da Solução

```
                    +------------------------------------+
                    |         <<Abstract Class>>         |
                    |          EstrategiaFrete           |
                    +------------------------------------+
                    | + calcular(pedido: Pedido): float  |
                    +------------------------------------+
                                       ^
                                       | (herança / contrato)
      +---------------+---------------+----------------+---------------+----------------+
      |               |               |                |               |                |
+-----------+   +----------+   +--------------------+  +--------------+  +------------+
| FreteSedex|   | FretePac |   | FreteTransportadora|  | FreteMotoboy |  | FreteDrone |
+-----------+   +----------+   +--------------------+  +--------------+  +------------+
```

```
                 (possui / delega para)
+------------+ -------------------------> +-------------------+
|   Pedido   | 1                        1 |  EstrategiaFrete  |
| (Contexto) |                            +-------------------+
+------------+
```

### Componentes do Padrão:
1. **Strategy (Interface Abstrata):** `EstrategiaFrete` define a assinatura comum que todos os algoritmos de frete devem seguir.
2. **Concrete Strategies (Estratégias Concretas):** `FreteSedex`, `FretePac`, `FreteTransportadora`, `FreteMotoboy` e `FreteDrone` encapsulam individualmente a fórmula de cálculo de cada modalidade.
3. **Context (Contexto):** `Pedido` mantém uma referência para um objeto `EstrategiaFrete` e delega a ele a responsabilidade do cálculo.
4. **Client (Cliente):** `teste-frete.py` instancia a estratégia desejada e a injeta no pedido antes de solicitar o cálculo.

---

## 3. Detalhamento de Cada Arquivo

### A. `estrategia_frete.py` (Interface e Estratégias Concretas)

* **Interface Abstrata (`EstrategiaFrete`):**
  Utiliza o módulo nativo `abc` (`ABC` e `@abstractmethod`) do Python para definir o contrato obrigatório:
  ```python
  class EstrategiaFrete(ABC):
      @abstractmethod
      def calcular(self, pedido: "Pedido") -> float:
          pass
  ```
* **Classes Concretas:**
  Cada classe herda de `EstrategiaFrete` e implementa sua respectiva fórmula de cálculo:
  * `FreteSedex`: `10.0 + (pedido.peso_kg * 1.5)`
  * `FretePac`: `5.0 + (pedido.peso_kg * 1.0)`
  * `FreteTransportadora`: `20.0 + (pedido.peso_kg * 3.0)`
  * `FreteMotoboy`: `15.0` (taxa fixa)
  * `FreteDrone`: `25.0` (taxa fixa)

### B. `pedido.py` (O Contexto)

A classe `Pedido` foi completamente simplificada:
* **Remoção de condicionais:** Todo o bloco `if/elif/else` foi eliminado.
* **Atributo privado e Setter:**
  ```python
  self._estrategia: Optional[EstrategiaFrete] = estrategia
  
  def set_estrategia(self, estrategia: EstrategiaFrete) -> None:
      self._estrategia = estrategia
  ```
* **Delegação limpa:** O método `calcular_frete()` não recebe mais parâmetros de tipo de frete. Ele valida a existência de uma estratégia e delega o cálculo passando a si mesmo (`self`) como parâmetro:
  ```python
  def calcular_frete(self) -> float:
      if self._estrategia is None:
          raise ValueError("Estratégia de frete não definida. Utilize set_estrategia() antes de calcular.")
      return self._estrategia.calcular(self)
  ```

### C. `teste-frete.py` (O Cliente)

O cliente agora utiliza **Injeção de Dependência**, configurando a estratégia no pedido:
```python
pedido = Pedido(peso_kg=2.5)

# O cliente escolhe a estratégia e a injeta no pedido
pedido.set_estrategia(FreteSedex())
print(f"Valor do frete SEDEX: R$ {pedido.calcular_frete():.2f}")

pedido.set_estrategia(FretePac())
print(f"Valor do frete PAC: R$ {pedido.calcular_frete():.2f}")
```

---

## 4. Teste de Extensibilidade e Validação do OCP (Passo 5)

Para validar se o princípio Aberto/Fechado foi de fato atingido:
1. Surgiu um novo requisito: entrega por **DRONE** (taxa fixa de R$ 25,00).
2. Criou-se apenas a nova classe `FreteDrone(EstrategiaFrete)` em `estrategia_frete.py`.
3. **A classe `Pedido` não precisou sofrer nenhuma alteração.**

Isso comprova que o sistema está **aberto para extensão** (adicionamos `FreteDrone`), mas **fechado para modificação** (a classe `Pedido` permaneceu intacta).

---

## 5. Como Executar os Testes

Execute o script de teste no terminal:
```bash
python teste-frete.py
```

### Saída Obtida:
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

---

## 6. Histórico de Commits do Projeto

| Commit | Mensagem do Commit | Descrição da Etapa |
| :--- | :--- | :--- |
| `1f3cdeb` | `feat: adiciona interface abstrata EstrategiaFrete (Passo 1)` | Criação da classe abstrata com contrato `calcular` |
| `f331e57` | `feat: cria classes concretas de frete (Passo 2)` | Implementação de `FreteSedex`, `FretePac`, `FreteTransportadora`, `FreteMotoboy` |
| `92e335f` | `refactor: refatora Pedido como Contexto do padrão Strategy (Passo 3)` | Eliminação de condicionais e delegação para a estratégia |
| `0491e22` | `refactor: atualiza cliente teste-frete.py para injetar estratégias (Passo 4)` | Adaptação do script cliente para injeção de dependência |
| `935114e` | `feat: adiciona frete por Drone testando extensibilidade do OCP (Passo 5)` | Criação do `FreteDrone` sem alterar a classe `Pedido` |
| `c74e369` | `docs: atualiza documentação com explicações detalhadas da refatoração (Passo 6)` | Atualização do README com a documentação do projeto |
