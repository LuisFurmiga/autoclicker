# AutoClicker 2.0

## README Multilíngue
Don't speak Portuguese? Visit: [![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/LuisFurmiga/Autoclicker/blob/main/languages/us/README.us.md)

¿No hablas portugués? Acceso: [![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/LuisFurmiga/Autoclicker/blob/main/languages/es/README.es.md)

---

## 🚀 Visão geral
O **AutoClicker 2.0** é uma ferramenta avançada para automação de cliques e teclas em janelas específicas.  
Ele foi totalmente reescrito em relação à versão 1.0, trazendo **suporte a múltiplos perfis, interface multilíngue e novas opções de personalização**.

Ideal para jogos, testes de software e qualquer tarefa repetitiva que exija interações rápidas e constantes com o mouse ou teclado.

---

## ✨ Novidades da versão 2.0
- ✅ **Perfis múltiplos** armazenados em `profiles.json`
  - Criar, renomear, excluir, importar e exportar (um ou todos os perfis).
  - Migração automática de `settings.json` (versão antiga) para `profiles.json`.
- ✅ **Interface reorganizada (Tkinter)**
  - Menu de **Idioma** (Português, Inglês, Espanhol).
  - Menu de **Perfis** (com seleção via radiobutton e opções de gerenciamento).
- ✅ **Automação completa**
  - Cliques esquerdo e direito independentes.
  - Envio de **teclas extras**, incluindo combinações (`ctrl+c`, `ctrl+shift+tab`, etc.).
- ✅ **Hotkeys globais**
  - `F1` → iniciar
  - `F2` → parar
- ✅ **Seleção de janela alvo**
  - Lista suspensa mostra todas as janelas abertas do sistema.
- ✅ **Mensagens e erros traduzidos** em três idiomas (i18n).
- ✅ **Interface reorganizada (Tkinter)**
  - Menu de **Idioma** (Português, Inglês, Espanhol).
  - Menu de **Perfis** (com seleção via radiobutton e opções de gerenciamento).
  - **Abas** separando **Mouse** e **Teclado** para facilitar a configuração.
- ✅ **Automação completa**
  - Cliques esquerdo e direito independentes.
  - Envio de **teclas extras**, incluindo combinações (`ctrl+c`, `ctrl+shift+tab`, etc.).

---

## 🧩 Parâmetros de Teclado
Na aba **Teclado**, além de `Teclas adicionais`, é possível ajustar:
- **Atraso da tecla (`key_delay`)**: tempo entre pressionar/soltar a tecla base.
- **Atraso dos modificadores (`modifier_delay`)**: tempo ao pressionar/soltar `ctrl/alt/shift`.
- **Intervalo entre combos (`extra_key_gap`)**: tempo entre envio de teclas/combos sucessivos.

---

## 📤 Perfis
- Criar quantos quiser.
- Exportar/importar perfis individuais ou todos de uma vez.

---

## 📂 Estrutura do projeto
```
autoclicker/
│── app.py                 # Ponto de entrada
│── controllers/
│   └── app_controller.py  # Lógica principal
│── models/
│   ├── settings.py        # Configuração de perfis
│   ├── auto_clicker.py    # Implementação do autoclicker
│   └── profiles.py        # Armazenamento de múltiplos perfis
│── views/
│   └── main_window.py     # Interface Tkinter
│── profiles.json          # Perfis do usuário
│── translations.json      # Traduções (pt, en, es)
│── requirements.py        # Instala dependências automaticamente
└── README.md              # Este documento
```

---

## ⚙️ Instalação
1. Clone o repositório:
    ```sh
    git clone https://github.com/LuisFurmiga/autoclicker.git
    ```
2. Acesse o diretório:
    ```sh
    cd autoclicker
    ```
3. Se ainda não tiver o Python instalado, consulte o guia [Python para Windows](https://github.com/LuisFurmiga/Autoclicker/blob/main/languages/pt-br/python_windows.pt-br.md).
4. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```
   ou use o instalador automático:
    ```sh
    python requirements.py
    ```

---

## 🎮 Como usar
1. Execute o programa:
    ```sh
    python app.py
    ```
2. Escolha a **janela alvo** no menu suspenso.
3. Ajuste os intervalos de clique, tempo de pressão e teclas extras.
4. Salve suas configurações em um **perfil**.
5. Use:
   - `F1` → **Iniciar**
   - `F2` → **Parar**

---

## 🌐 Idiomas suportados
- 🇧🇷 Português  
- 🇺🇸 Inglês  
- 🇪🇸 Espanhol  

A troca de idioma é feita diretamente no **menu da interface**.

---

## 📤 Perfis
- Criar quantos quiser.
- Exportar/importar perfis individuais ou todos de uma vez.
- Perfis são salvos em `profiles.json`.

---

## 🛠️ Dependências
- [keyboard](https://pypi.org/project/keyboard/) → hotkeys globais  
- [pywin32](https://pypi.org/project/pywin32/) → manipulação de janelas e eventos do Windows  

---

## ⚠️ Observações importantes
- Execute como **Administrador** se os atalhos globais não funcionarem dentro do jogo.  
- O programa é **Windows-only** devido ao uso da biblioteca `pywin32`.  

---

## 📜 Licença
Este projeto é de código aberto sob a licença [MIT](https://opensource.org/licenses/MIT).
