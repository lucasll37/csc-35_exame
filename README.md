# **🚁 Flying Ad Hoc Network (FANET) 🚀**  
💡 **Uma simulação de FANET (Flying Ad Hoc Network), projetada para estudar comunicação segura, dinâmica descentralizada e ataques cibernéticos em redes de drones.**

---

## **📋 Índice**  
- [**🚁 Flying Ad Hoc Network (FANET) 🚀**](#-flying-ad-hoc-network-fanet-)
  - [**📋 Índice**](#-índice)
  - [**📝 Sobre o Projeto**](#-sobre-o-projeto)
  - [**🌍 Cenário e Contexto**](#-cenário-e-contexto)
  - [**📂 Estrutura do Projeto**](#-estrutura-do-projeto)
  - [**⚙️ Arquitetura e Processos**](#️-arquitetura-e-processos)
    - [🛠️ **Processo de Comunicação**](#️-processo-de-comunicação)
    - [🕹️**Decisão Descentralizada**](#️decisão-descentralizada)
  - [📜 **Pré-requisitos**](#-pré-requisitos)
  - [**Instalação**](#instalação)
  - [🚀 **Como Usar**](#-como-usar)
  - [🎮 **Funcionalidades**](#-funcionalidades)
  - [🔐 **Ataques e Segurança**](#-ataques-e-segurança)
    - [💀 **Ataques Simulados:**](#-ataques-simulados)
    - [💡 **Medidas de Segurança:**](#-medidas-de-segurança)
  - [🌟 **Melhorias Futuras**](#-melhorias-futuras)

---

## **📝 Sobre o Projeto**  
Este projeto simula uma FANET (Flying Ad Hoc Network) com:  
- **Movimentação de drones:** Decisão descentralizada de missões.  
- **Comunicação criptografada:** Segurança e resiliência contra ataques.  
- **Ataques simulados:** Investigação de cenários de interceptação.  

**🚀 Tecnologias usadas:**  
- Python  
- Pygame  
- NumPy  
- Cryptography  

---

## **🌍 Cenário e Contexto**  
Os drones operam em três cenários principais:  
1. 🏔️ **Desastres naturais:** Entrega de kits médicos em áreas de emergência.  
2. 🛶 **Regiões de difícil acesso:** Logística em áreas remotas.  
3. 🚦 **Zonas urbanas densas:** Navegação em tráfego intenso.  

💡 **Dinâmica da Rede:**  
- 🚁 **Drones em alerta:** 6 drones aguardam em voo estacionário.  
- 📍 **Missão:** Identificar o drone mais próximo do ponto de interesse.  
- 🔗 **Comunicação restrita:** Cada drone fala apenas com seus dois vizinhos mais próximos.  
- 🛑 **Persistência:** Após atingir o ponto, o drone espera novas ordens.  

---

## **📂 Estrutura do Projeto**  
| Arquivo/Classe         | Função/Descrição                                                                                   |  
|-------------------------|---------------------------------------------------------------------------------------------------|  
| **`main.py`**           | Ponto de entrada; inicializa componentes e executa o loop principal.                             |  
| **`adhoc.py`**          | Gerencia a rede ad hoc (drones, hackers, estação base); renderiza a tela.                        |  
| **`drone.py`**          | Define a classe Drone, responsável por movimentação e comunicação.                               |  
| **`baseStationControl.py`** | Gerencia o envio/recebimento de mensagens pela estação base (GCS).                            |  
| **`hacker.py`**         | Simula hackers; intercepta e transmite mensagens capturadas.                                     |  
| **`message.py`**        | Define mensagens trocadas; inclui criptografia/descriptografia.                                  |  
| **`encryption.py`**     | Implementa criptografia simétrica.                                                               |  
| **`globals.py`**        | Define constantes globais (dimensões, cores, etc.).                                              |  
| **`debug.ipynb`**       | Notebook Jupyter para depuração e análise.                                                       |  
| **`requirements.txt`**  | Lista de dependências.                                                                           |  
| **`Makefile`**          | Automação para configurar o ambiente de desenvolvimento.                                         |  

---

## **⚙️ Arquitetura e Processos**  

### 🛠️ **Processo de Comunicação**  
- **`DISCOVER:`** A estação base localiza o drone mais próximo de um ponto de interesse.  
- **`RETURN:`** O drone mais próximo comunica sua identificação.  
- **`EXECUTE:`** A missão é atribuída ao drone mais próximo.  
- **`COMPLETE:`** Confirmação de que o ponto foi alcançado.  
- **`FINISH:`** Início de uma nova missão.  

**Exemplo de Criação e Propagação de Mensagem:**  
```python
# Exemplo de envio de mensagem DISCOVER
message = Message(type="DISCOVER", target=target_point, origin=self)
self.adhoc.broadcast(message)
```

### 🕹️**Decisão Descentralizada**
Cada drone calcula localmente a menor distância ao ponto de interesse. Mensagens são propagadas apenas para os vizinhos mais próximos.

## 📜 **Pré-requisitos**
- Python 3.8 ou superior.  
- Dependências principais: NumPy, Pygame, Cryptography.

## **Instalação**
Clone o repositório e configure um ambiente virtual:

```bash	
git clone https://github.com/lucasll37/csc-35_exame.git
cd csc-35_exame/src
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🚀 **Como Usar**
Ative o ambiente virtual e execute o script principal:

```bash
source .venv/bin/activate
python main.py
```

Interaja com a simulação.

## 🎮 **Funcionalidades**

- **Simulação visual:** Renderização dinâmica da FANET em Pygame.
- **Mensagens criptografadas:** Comunicação segura entre drones e estação base.
- **Logs automáticos:** Geração de logs em cada etapa da simulação.
- **Robustez:** Algoritmo resiliente que minimiza mensagens desnecessárias.

## 🔐 **Ataques e Segurança**

### 💀 **Ataques Simulados:**

- **Replay Attack:** Um hacker armazena mensagens e tenta inundar a rede.
- **Ativação Maliciosa:** Envio de pacotes que simulam mensagens válidas para drones específicos.

### 💡 **Medidas de Segurança:**

- **Nonce por Missão:** Cada missão tem um ID único, dificultando ataques por replay.
- **Chave Simétrica Inicial:** Garantia de comunicação segura em canal físico.

## 🌟 **Melhorias Futuras**

- 🔧**Otimização do Algoritmo**: Melhorar a escolha do drone mais próximo.
- 📊**Análise de Desempenho**: Avaliar escalabilidade e latência em redes maiores.
- 🛡️**Segurança Avançada**: Implementar detecção de intrusão e bloqueio de drones maliciosos.
