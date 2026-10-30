# 🐉 Dragon's Crown Pro (Recomp PC) — Tradução PT-BR

> Tradução **não-oficial** para **Português do Brasil** de *Dragon's Crown Pro* na versão **recompilada para PC / Steam Deck** ([saulob/dragons-crown-pro-pc](https://github.com/saulob/dragons-crown-pro-pc)).

<p align="center">
  <img alt="Idioma" src="https://img.shields.io/badge/idioma-Portugu%C3%AAs%20(BR)-009c3b">
  <img alt="Plataforma" src="https://img.shields.io/badge/plataforma-PC%20%2B%20Steam%20Deck-1b2838">
  <img alt="Versão" src="https://img.shields.io/badge/vers%C3%A3o-1.1-8b0000">
  <img alt="Uso" src="https://img.shields.io/badge/uso-n%C3%A3o--comercial-important">
</p>

---

## 📜 Sobre

O recomp roda a versão de PS4 (v1.03, US) de *Dragon's Crown Pro* nativamente no PC. Esta tradução troca os textos em inglês do jogo pelo português do Brasil: história, narração do Mestre, missões, habilidades, itens, menus e tutoriais.

Basta manter o idioma do jogo em **English** (o padrão) — com a tradução instalada, ele aparece em português.

> ⚠️ **Aviso:** esta é uma **tradução amadora**, feita por um fã, e **pode conter erros** — typos, trechos com sentido ligeiramente diferente do original, ou alguma linha que fique apertada na caixa de texto. Não é um trabalho profissional/oficial. Se encontrar algum erro, abra uma [*issue*](../../issues) que eu corrijo em versões futuras. 🙂

---

## 🎮 O que foi traduzido

**12.272 textos** (cerca de 370 mil caracteres) em 15 arquivos de mensagens do jogo:

| Parte do jogo | Arquivo |
|------|---------|
| 📖 História, narração do Mestre e cutscenes | `EventMsg` |
| 🧭 Menus, opções, acampamento, pausa, seleção de personagem, tutoriais e o final | `SystemMsg`, `Tutorial` |
| 📜 Missões da Guilda dos Aventureiros (títulos, pedidos, objetivos e resultados) | `ChallengeQuest` |
| ✨ Habilidades das 6 classes (nomes, efeitos e descrições) | `AbilityList` |
| 🗡️ Itens, equipamentos, efeitos mágicos e prefixos/sufixos | `ItemList`, `CustomItem` |
| 👹 Inimigos, chefes e objetos | `ObjectParam` |
| 💀 Falas dos aventureiros ressuscitados | `DefaultBone` |
| 🖼️ Galeria de Tesouros e epílogos | `TreasureArt` |
| ⛪ Orações e bênçãos do Templo, pontuação | `Temple`, `BonusScore`, `RoundContinue` |
| 🎬 Cargos dos créditos | `StaffRollMsg` |

A fonte do jogo já tem todos os acentos do português (ã, õ, ç, ê...), então nada de letras faltando.

### 🚫 O que **não** foi traduzido (de propósito)

| Item | Por quê |
|------|---------|
| Nomes de personagens e de aventureiros (Lucain, Rannie, Morgan...) | Nomes próprios |
| Nomes de pessoas e empresas nos créditos | Nomes próprios |
| Textos desenhados em imagens (logos, alguns títulos) | Ficam para uma versão futura |
| Textos de depuração (debug) do jogo | Nunca aparecem jogando |

---

## 💾 Instalação

> **Requisitos:** o recomp do *Dragon's Crown Pro* já instalado e funcionando (jogo v1.03, US). O instalador usa **Python 3** — no **Steam Deck / Linux** já vem instalado; no **Windows**, se não tiver, baixe em [python.org/downloads](https://www.python.org/downloads/) marcando *"Add python.exe to PATH"*.

### 🪟 Windows

1. Baixe o `.zip` da [última versão](../../releases/latest) e **descompacte**.
2. **Feche o jogo e o launcher.**
3. Dê **duplo-clique** em `instalar_traducao_windows.bat`.
4. Ele encontra o jogo sozinho e aplica. *(Se não achar, arraste a pasta do jogo para a janela e pressione ENTER — ou arraste a pasta do jogo em cima do `.bat`.)*
5. Pronto! Abra o jogo pelo `dcp-loader.exe` com o idioma em **English**.

### 🎮 Steam Deck / Linux

1. **Feche o jogo** e vá para o **Modo Desktop**.
2. Copie a pasta descompactada para o Deck (ex.: `~/Downloads`).
3. Abra o **Konsole** nessa pasta e rode:
   ```bash
   chmod +x instalar_traducao_linux.sh
   ./instalar_traducao_linux.sh
   ```
   *(ou `./instalar_traducao_linux.sh "/caminho/da/pasta/do/jogo"`)*

O instalador **não duplica** o `DRACRO_US.CPK` (~870 MB): ele anexa os textos traduzidos ao fim do arquivo e repõe o índice, lendo tudo de volta para conferir. Se algo não bater, ele desfaz sozinho.

**Atualizando a tradução?** Rode o instalador da versão nova por cima: ele troca a anterior sem aumentar o arquivo.

---

## ↩️ Como reverter

Dê duplo-clique em `desinstalar_traducao_windows.bat` (ou rode `./desinstalar_traducao_linux.sh`). O `DRACRO_US.CPK` volta **exatamente** ao que era antes — o índice original fica guardado em `DRACRO_US.CPK.ptbr.undo`, ao lado do jogo (não apague esse arquivo).

### 🎮 Botões de Xbox (opção *Controller prompts* do launcher)

O launcher também modifica o `DRACRO_US.CPK` para trocar os ícones de botões.

- Instalou a tradução **antes** de escolher os botões de Xbox? Pode trocar os botões à vontade, a tradução continua.
- Os botões de Xbox **já estavam** ativos quando instalou a tradução? Voltar para PlayStation remove a tradução — é só rodar o instalador de novo.
- Para desinstalar a tradução com os botões de Xbox aplicados depois dela, volte antes os botões para PlayStation no launcher (o desinstalador avisa).

Se você **reinstalar ou atualizar o jogo** pelo launcher, rode o instalador da tradução de novo.

---

## 🛠️ Como foi feito (resumo técnico)

1. Os textos ficam em arquivos `msgsheet/*_US.fms` (formato **FMSB** da Vanillaware: cabeçalho, tabela e strings UTF-8) dentro do `DRACRO_US.CPK` (pacote **CRI CPK**).
2. Os textos foram extraídos, traduzidos e reempacotados mantendo **todos os códigos de controle** do jogo (cores `@c(n)`, ícones de botão `@#(n)`, pausas `@w(n)`, variáveis `##(NOME)` e `%d`/`%s`), conferidos linha a linha contra o original.
3. O instalador anexa os `.fms` ao fim do CPK e reaponta as entradas do índice (TOC), no mesmo formato de registro de desfazer que o launcher usa.

---

## ⚖️ Licença e uso

Esta é uma **tradução de fã**, feita **sem fins lucrativos** e **sem qualquer afiliação** com a Atlus, a Vanillaware ou a Sega.

- ✅ **Pode** baixar, usar e compartilhar **gratuitamente**.
- ✅ **Pode** repostar, desde que **credite** o autor e **mantenha** este aviso.
- ❌ **É proibido vender, cobrar, monetizar ou lucrar** de qualquer forma com esta tradução.
- ❌ **É proibido distribuir os arquivos do jogo.** Compartilhe **apenas o patch** deste repositório — nunca o `DRACRO_US.CPK` ou outros arquivos originais.

*Dragon's Crown* e todos os nomes relacionados são marcas registradas da **Atlus / Vanillaware / Sega**. Este projeto não é oficial e não substitui a compra do jogo. Veja [LICENSE.txt](LICENSE.txt).

---

## 🙏 Créditos

**Tradução e ferramentas:** **Wender_sky** *(Steam)*

Recomp para PC: [saulob/dragons-crown-pro-pc](https://github.com/saulob/dragons-crown-pro-pc).

Com a tradução instalada, o crédito aparece na tela de título, abaixo de "Pressione o botão".
