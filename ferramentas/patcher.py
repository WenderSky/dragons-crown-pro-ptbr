#!/usr/bin/env python3
# Licenca: GNU GPL v2 (usa o cpk.py do projeto dragons-crown-pro-pc); ver LICENSE-GPL-2.0.txt.
"""Instalador da traducao PT-BR do Dragon's Crown Pro (recomp PC). Windows e Linux/Steam Deck, so biblioteca padrao.

    patcher.py apply  [jogo] [pasta_traducao]   instala (ou atualiza) a traducao
    patcher.py revert [jogo]                    volta o DRACRO_US.CPK ao estado anterior a traducao
    patcher.py status [jogo]                    diz se a traducao esta instalada

[jogo] e o DRACRO_US.CPK ou qualquer pasta acima dele; sem ele, o patcher procura nos lugares de costume.

Como funciona: os .fms traduzidos sao anexados ao fim do DRACRO_US.CPK e as linhas deles no TOC passam a apontar
para la. Nada dos dados originais e sobrescrito. O registro de desfazer fica em DRACRO_US.CPK.ptbr.undo, no mesmo
formato do launcher (DCPUNDO1: tamanho original, TOC e cabecalho originais, nomes dos arquivos trocados). O nome e
diferente do DRACRO_US.CPK.undo do launcher de proposito: o launcher trata a existencia daquele arquivo como
"botoes de Xbox instalados" e o desfaz quando se troca o estilo de botoes.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import cpk as cpklib

ARCHIVE_NAME = 'DRACRO_US.CPK'
UNDO_SUFFIX = '.ptbr.undo'
LAUNCHER_UNDO_SUFFIX = '.undo'
UNDO_MAGIC = b'DCPUNDO1'


# ------------------------------------------------------------------ registro de desfazer

def undo_path(cpk_path):
    return cpk_path.with_name(cpk_path.name + UNDO_SUFFIX)


def launcher_undo_path(cpk_path):
    return cpk_path.with_name(cpk_path.name + LAUNCHER_UNDO_SUFFIX)


def write_undo(path, rec):
    names = '\n'.join(rec['names']).encode('utf-8')
    path.write_bytes(UNDO_MAGIC
                     + struct.pack('<QQI', rec['original_len'], rec['toc_pos'], len(rec['toc'])) + rec['toc']
                     + struct.pack('<QI', rec['header_pos'], len(rec['header'])) + rec['header']
                     + struct.pack('<I', len(names)) + names)


def read_undo(path):
    b = path.read_bytes()
    if b[:8] != UNDO_MAGIC:
        raise ValueError(f'{path.name}: registro de desfazer invalido')
    original_len, toc_pos, toc_len = struct.unpack_from('<QQI', b, 8)
    pos = 28
    toc = b[pos:pos + toc_len]; pos += toc_len
    header_pos, header_len = struct.unpack_from('<QI', b, pos); pos += 12
    header = b[pos:pos + header_len]; pos += header_len
    names = []
    if pos + 4 <= len(b):
        n = struct.unpack_from('<I', b, pos)[0]
        names = [x for x in b[pos + 4:pos + 4 + n].decode('utf-8', 'replace').split('\n') if x]
    return dict(original_len=original_len, toc_pos=toc_pos, toc=toc, header_pos=header_pos, header=header,
                names=names)


def restore(cpk_file, rec):
    """Poe de volta o TOC e o cabecalho do registro e corta o arquivo no tamanho original."""
    with open(cpk_file, 'r+b') as f:
        f.seek(rec['toc_pos'])
        f.write(rec['toc'])
        f.seek(rec['header_pos'])
        f.write(rec['header'])
        f.truncate(rec['original_len'])


def current_bytes(cpk_file, pos, length):
    with open(cpk_file, 'rb') as f:
        f.seek(pos)
        return f.read(length)


def is_translation_record(rec):
    """Um DRACRO_US.CPK.undo deixado pela versao antiga do instalador (so trocou msgsheet/*.fms)."""
    return bool(rec['names']) and all(n.lower().startswith('msgsheet/') and n.lower().endswith('.fms')
                                      for n in rec['names'])


def installed(cpk_file, rec):
    """A traducao esta no arquivo: o tamanho passa do original e o TOC nao e mais o do registro."""
    size = cpk_file.stat().st_size
    return size > rec['original_len'] and current_bytes(cpk_file, rec['toc_pos'], len(rec['toc'])) != rec['toc']


def launcher_on_top(cpk_file, rec):
    """O launcher aplicou os botoes de Xbox depois da traducao: o registro dele parte de um arquivo ja traduzido."""
    lu = launcher_undo_path(cpk_file)
    if not lu.exists():
        return False
    try:
        return read_undo(lu)['original_len'] > rec['original_len']
    except (ValueError, struct.error):
        return False


# ------------------------------------------------------------------ localizar o jogo

def find_game_cpk(user_path=None):
    if user_path:
        clean = str(user_path).strip().strip('\'"')
        if clean.startswith('file://'):
            clean = clean[7:]
        p = Path(clean)
        if p.is_file() and p.name.upper() == ARCHIVE_NAME:
            return p
        if p.is_dir():
            for c in (p / 'game' / 'prepared' / 'v1.03' / ARCHIVE_NAME,
                      p / 'Windows' / 'game' / 'prepared' / 'v1.03' / ARCHIVE_NAME,
                      p / 'prepared' / 'v1.03' / ARCHIVE_NAME,
                      p / 'v1.03' / ARCHIVE_NAME,
                      p / ARCHIVE_NAME):
                if c.is_file():
                    return c
            for c in p.rglob(ARCHIVE_NAME):
                return c
        return None

    for c in (SCRIPT_DIR.parent / 'game' / 'prepared' / 'v1.03' / ARCHIVE_NAME,
              SCRIPT_DIR.parent.parent / 'game' / 'prepared' / 'v1.03' / ARCHIVE_NAME,
              SCRIPT_DIR.parent.parent / 'Windows' / 'game' / 'prepared' / 'v1.03' / ARCHIVE_NAME,
              Path(r"E:\Recomps\Dragon's Crown Pro PS4 ver\Windows\game\prepared\v1.03") / ARCHIVE_NAME,
              Path.home() / '.local/share/DragonsCrownProPC/game/prepared/v1.03' / ARCHIVE_NAME):
        if c.is_file():
            return c
    return None


def locate(game_path):
    """find_game_cpk, perguntando o caminho quando nao acha sozinho e ha alguem no terminal."""
    cpk_file = find_game_cpk(game_path)
    if cpk_file:
        return cpk_file
    print(f'{ARCHIVE_NAME} nao encontrado' + (f' em: {game_path}' if game_path else ' nos locais padrao.'))
    if not sys.stdin or not sys.stdin.isatty():
        return None
    try:
        typed = input('Arraste aqui a pasta do jogo (ou o DRACRO_US.CPK) e tecle Enter: ')
    except EOFError:
        return None
    cpk_file = find_game_cpk(typed) if typed.strip() else None
    if not cpk_file:
        print(f'Erro: {ARCHIVE_NAME} nao encontrado em: {typed}')
    return cpk_file


def unshare(cpk_file):
    """A instalacao do launcher pode criar o arquivo como hard link de outra pasta; escrever nele mudaria as duas
    copias. Como o launcher, damos ao arquivo uma copia propria antes de mexer."""
    try:
        links = os.stat(cpk_file).st_nlink
    except OSError:
        return
    if links <= 1:
        return
    print(f'{cpk_file.name} e um hard link; criando uma copia propria antes de modificar (pode demorar)...')
    tmp = cpk_file.with_name(cpk_file.name + '.copy')
    shutil.copyfile(cpk_file, tmp)
    os.replace(tmp, cpk_file)


# ------------------------------------------------------------------ aplicar / reverter

def collect_mod_files(mod_dir):
    files = {}
    for p in sorted(mod_dir.rglob('*')):
        if p.is_file():
            files[p.relative_to(mod_dir).as_posix().lower()] = p
    return files


def migrate_old_record(cpk_file):
    """A versao antiga do instalador gravava DRACRO_US.CPK.undo, que o launcher confunde com os botoes de Xbox.
    Se esse registro for so da traducao, desfaz por ele e o remove; a instalacao recomeca do original.
    Devolve True se removeu uma instalacao antiga."""
    old = launcher_undo_path(cpk_file)
    if not old.exists():
        return False
    try:
        rec = read_undo(old)
    except (ValueError, struct.error):
        return False
    if not is_translation_record(rec):
        return False   # e do launcher (botoes de Xbox): fica onde esta
    if cpk_file.stat().st_size < rec['original_len']:
        print(f'Registro antigo {old.name} nao corresponde mais ao arquivo; ignorando-o.')
    else:
        print(f'Removendo a instalacao anterior (registro antigo {old.name})...')
        restore(cpk_file, rec)
    old.unlink()
    return True


def apply_translation(game_path, mod_dir):
    cpk_file = locate(game_path)
    if not cpk_file:
        return False
    mod_dir = Path(mod_dir).resolve()
    mod_files = collect_mod_files(mod_dir)
    if not mod_files:
        print(f'Erro: nenhum arquivo de traducao em {mod_dir}')
        return False
    print(f'Jogo: {cpk_file}')

    unshare(cpk_file)
    migrate_old_record(cpk_file)

    undo = undo_path(cpk_file)
    rec = None
    if undo.exists():
        rec = read_undo(undo)
        if not installed(cpk_file, rec):
            # O arquivo foi reinstalado, ou outro patch o restaurou: o registro nao vale mais.
            rec = None
        elif not launcher_on_top(cpk_file, rec):
            print('Atualizando a traducao ja instalada...')
            restore(cpk_file, rec)
            rec = None
        # Com os botoes de Xbox do launcher por cima, nao da para cortar o arquivo: os .fms novos so sao
        # anexados de novo e o registro original (anterior a traducao) e mantido.

    arc = cpklib.Cpk(cpk_file)
    try:
        targets = []
        for e in arc.entries:
            p = mod_files.get(e['path'].lower())
            if p:
                targets.append((e, p))
        missing = sorted(set(mod_files) - {e['path'].lower() for e, _ in targets})
        if missing:
            print(f'Erro: arquivos que nao existem no {ARCHIVE_NAME}: ' + ', '.join(missing))
            return False

        toc_pos = arc.toc_offset + 16
        header_pos = 16
        original_toc = arc.toc.packet_bytes()
        if rec is None:
            rec = dict(original_len=cpk_file.stat().st_size, toc_pos=toc_pos, toc=original_toc,
                       header_pos=header_pos, header=arc.header.packet_bytes(), names=[])
        rec['names'] = sorted(set(rec['names']) | {e['path'] for e, _ in targets})
        write_undo(undo, rec)

        align = arc.align or 0x800
        print(f'\nInstalando {len(targets)} arquivos:')
        with open(cpk_file, 'r+b') as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            for e, p in targets:
                data = p.read_bytes()
                pos = (pos + align - 1) // align * align
                f.seek(pos)
                f.write(data)
                row = e['row']
                arc.toc.set_number(row, 'FileOffset', pos - arc.toc_base)
                arc.toc.set_number(row, 'FileSize', len(data))
                if (row, 'ExtractSize') in arc.toc.positions:
                    arc.toc.set_number(row, 'ExtractSize', len(data))
                print(f'  [+] {e["path"]} ({len(data)} bytes)')
                pos += len(data)
            new_toc = arc.toc.packet_bytes()
            assert len(new_toc) == len(original_toc), 'o tamanho do TOC mudou'
            f.seek(toc_pos)
            f.write(new_toc)
            h = arc.header.rows[0]
            for flag in ('EnableTocCrc', 'EnableFileCrc'):
                if h.get(flag) and (0, flag) in arc.header.positions:
                    arc.header.set_number(0, flag, 0)
            f.seek(header_pos)
            f.write(arc.header.packet_bytes())
    finally:
        arc.f.close()

    # Confere lendo de volta pelo TOC novo; se algo nao bater, desfaz.
    check = cpklib.Cpk(cpk_file)
    try:
        bad = [e['path'] for e, p in targets if check.read(check.entries[e['row']]) != p.read_bytes()]
    finally:
        check.f.close()
    if bad:
        print('Erro: a verificacao falhou para ' + ', '.join(bad) + '; desfazendo.')
        restore(cpk_file, rec)
        undo.unlink()
        return False
    print(f'\nSucesso! {len(targets)} arquivos traduzidos instalados e verificados.')
    return True


def revert_translation(game_path):
    cpk_file = locate(game_path)
    if not cpk_file:
        return False
    print(f'Jogo: {cpk_file}')
    migrated = migrate_old_record(cpk_file)

    undo = undo_path(cpk_file)
    if not undo.exists():
        if migrated:
            print('Sucesso! A traducao foi removida; o jogo voltou ao original em ingles.')
            return True
        print('A traducao nao esta instalada (nenhum registro de desfazer encontrado).')
        return False
    rec = read_undo(undo)
    if not installed(cpk_file, rec):
        print('A traducao ja nao estava instalada; removendo o registro de desfazer que sobrou.')
        undo.unlink()
        return True
    if launcher_on_top(cpk_file, rec):
        print('Erro: os botoes de Xbox foram aplicados pelo launcher depois da traducao.\n'
              'No launcher, volte "Controller prompts" para PlayStation e rode o desinstalador de novo.')
        return False
    print('Restaurando o arquivo original...')
    restore(cpk_file, rec)
    undo.unlink()
    print('Sucesso! O jogo voltou ao original em ingles.')
    return True


def status(game_path):
    cpk_file = find_game_cpk(game_path)
    if not cpk_file:
        print(f'{ARCHIVE_NAME} nao encontrado.')
        return False
    undo = undo_path(cpk_file)
    on = undo.exists() and installed(cpk_file, read_undo(undo))
    print(f'{cpk_file}: traducao {"INSTALADA" if on else "nao instalada"}')
    return on


def main():
    try:
        sys.stdout.reconfigure(errors='replace')
    except (AttributeError, ValueError):
        pass
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ('apply', 'revert', 'restore', 'status'):
        print(__doc__)
        sys.exit(2)
    action = sys.argv[1].lower()
    game_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip() else None
    if action == 'apply':
        mod_dir = sys.argv[3] if len(sys.argv) > 3 else str(SCRIPT_DIR.parent / 'arquivos_traducao')
        ok = apply_translation(game_path, mod_dir)
    elif action in ('revert', 'restore'):
        ok = revert_translation(game_path)
    else:
        ok = status(game_path)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
