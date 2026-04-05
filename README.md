# 📡 Visualizador de Funções e Fasores — Circuitos Elétricos II

Aplicação desktop desenvolvida em Python para auxílio ao estudo de **Circuitos Elétricos II**, permitindo a visualização interativa de funções senoidais no domínio do tempo e diagramas fasoriais no plano complexo.

---

## ✨ Funcionalidades

### 🌊 Visualizador de Funções Senoidais
- Adicione, edite e remova funções do tipo **A·cos(ωt + θ)**
- Controle individual de **amplitude (A)**, **frequência angular (ω)** e **ângulo de fase (θ)**
- Defina o intervalo de plotagem em graus (com presets: 0°–360°, 0°–720°, −360°–360°, −720°–720°)
- Eixo X com ticks adaptativos conforme o intervalo selecionado
- Suporte a múltiplas funções simultâneas com cores distintas e legenda
- Duplo clique na lista para editar rapidamente uma função

### 📐 Diagrama Fasorial (Plano Fasorial)
- Janela modal dedicada ao plano complexo
- Adicione fasores por **magnitude** e **ângulo (graus)**
- Edite ou remova fasores individualmente
- Representação com setas coloridas, eixos cartesianos e legenda
- Escala automática baseada no maior fasor presente

---

## 🖥️ Interface

A aplicação é dividida em duas telas principais:

| Tela | Descrição |
|---|---|
| **FasorPlotter** | Janela principal com lista de funções e gráfico senoidal embutido |
| **PhasorDiagramApp** | Janela modal com o plano fasorial interativo |

---

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado e as seguintes bibliotecas:

```bash
pip install matplotlib numpy
```

> `tkinter` já vem incluso na instalação padrão do Python.

### Execução

```bash
python Codigo_de_ce2.py
```

---

## 📦 Dependências

| Biblioteca | Uso |
|---|---|
| `tkinter` / `ttk` | Interface gráfica (GUI) |
| `matplotlib` | Plotagem dos gráficos |
| `numpy` | Geração dos arrays de tempo e cálculo das funções |
| `cmath` | Conversão polar → retangular para os fasores |
| `math` | Funções matemáticas auxiliares |

---

## 🧮 Modelo Matemático

As funções senoidais seguem o modelo:

$$f(t) = A \cdot \cos(\omega t + \theta)$$

Onde:
- **A** — Amplitude
- **ω** — Frequência angular em rad/s
- **θ** — Ângulo de fase em graus (convertido internamente para radianos)

Os fasores são representados na forma polar **M∠θ** e convertidos para o plano cartesiano via `cmath.rect(magnitude, angle_rad)`.

---

## 📂 Estrutura do Projeto

```
.
└── Codigo_de_ce2.py   # Arquivo principal com toda a aplicação
```

---

## 🎓 Contexto

Desenvolvido como ferramenta de apoio para a disciplina de **Circuitos Elétricos II** do curso de Engenharia Elétrica da **UFCG** (Universidade Federal de Campina Grande).

---

## 📄 Licença

Este projeto é de uso acadêmico livre.
