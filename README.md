# DesertPatrol

Jogo de reconhecimento aéreo no deserto, desenvolvido em Python com Panda3D.
Você pilota um Supermarine Spitfire em missões de vigilância: identificar
contrabando, contar aeronaves inimigas e reportar ao comando.

**Autor:** Arthur Martins

---

## Requisitos

- Python 3.10 ou superior
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes recomendado)
  ou `pip` tradicional

## Dependências (em `requirements.txt`)

- `panda3d` — motor 3D
- `panda3d-simplepbr` — renderização PBR (sombreamento físico)
- `panda3d-gltf` — carregamento de modelos `.glb` / `.gltf`

---

## Como rodar

### Opção 1 — com `uv` (recomendado)

```bash
uv run --with-requirements requirements.txt python main.py
```

Ou passando as dependências diretamente:

```bash
uv run --with panda3d --with panda3d-simplepbr --with panda3d-gltf python main.py
```

### Opção 2 — com `pip` + venv

```bash
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt
python main.py
```

---

## Controles

| Tecla       | Ação                  |
|-------------|------------------------|
| Seta cima   | Subir / acelerar       |
| Seta baixo  | Descer / desacelerar   |
| Seta esq.   | Virar para esquerda    |
| Seta dir.   | Virar para direita     |
| `1`         | Câmera livre (debug)   |
| `s`         | Salvar screenshot      |

---

## Missões

1. **Rota de Contrabando** — Sobrevoe o deserto e conte os pacotes de
   cocaína espalhados pelos contrabandistas. A quantidade muda a cada
   partida.
2. **Infiltração Nômade** — Helicópteros não identificados pousaram em
   dois pontos distintos. Conte o total de aeronaves avistadas.
3. **Treino** — Familiarize-se com os controles antes do campo.

Cada missão tem tempo limitado. Ao final, responda à pergunta de debrief
para reportar suas observações.

---

## Estrutura do projeto

```
main.py              # Ponto de entrada e FSM de estados do jogo
engine.py            # Setup do Panda3D, iluminação, menus base
mission_loader.py    # Parser de arquivos .mission e gerador aleatório
mission_menu.py      # Tela de seleção de missão
briefing.py          # Tela de instruções pré-missão
cockpit_hud.py       # HUD durante o voo
report.py            # Tela de debrief com perguntas
settings.py          # Tela de configurações
models/              # Modelos 3D (.egg, .glb, texturas)
vfx/                 # Efeitos de partícula (.ptf)
```

---

## Notas

- Se o jogo travar com erro de `simplepbr` ou `gltf`, instale as
  dependências do `requirements.txt`.
- O motor de partículas do Panda3D precisa estar habilitado (já é feito
  automaticamente no `GameBase`).
- Para desativar o PBR e rodar em hardware mais limitado, edite
  `engine.py` e troque `simplepbr.init()` por `render.setShaderAuto()`.
