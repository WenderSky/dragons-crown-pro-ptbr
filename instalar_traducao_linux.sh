#!/usr/bin/env bash
# =====================================================================
#   INSTALAR TRADUCAO PT-BR - DRAGON'S CROWN PRO (STEAM DECK / LINUX)
# =====================================================================
# Uso: ./instalar_traducao_linux.sh [pasta do jogo ou DRACRO_US.CPK]
# Sem argumento, o patcher procura o jogo sozinho e, se nao achar, pergunta.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERRO] python3 nao encontrado."
    exit 1
fi

echo "====================================================================="
echo "  INSTALAR TRADUCAO PT-BR - DRAGON'S CROWN PRO (Steam Deck / Linux)"
echo "====================================================================="
echo ""

python3 "$SCRIPT_DIR/ferramentas/patcher.py" apply "${1:-}" "$SCRIPT_DIR/arquivos_traducao"
status=$?
if [ $status -eq 0 ]; then
    echo ""
    echo "[SUCESSO] Traducao PT-BR instalada! No launcher, mantenha o idioma em English."
else
    echo ""
    echo "[ERRO] A traducao nao foi instalada. Veja a mensagem acima."
fi
exit $status
