#!/usr/bin/env python3
"""Control de integridad de una base de asignaciones presupuestarias.

Uso:  python3 control-asignaciones.py archivo.csv [--ref ref4.json]

Comprueba cuatro propiedades. Devuelve código de salida 1 si alguna falla,
para poder encadenarlo en un proceso automático.

  1. Partición por nivel de gobierno. Los anexos 5, 6 y 7 cubren conjuntos
     de pliegos disjuntos, porque cada uno corresponde a un nivel distinto.
     Una intersección significa un error de lectura.
  2. Contención del corte transversal. El anexo 8 reorganiza por programa
     presupuestal dinero ya consignado en los anexos 6 y 7, y el anexo A
     reparte dinero del anexo 5. Ninguno puede exceder, en un pliego dado,
     el total que ese pliego tiene en su anexo de origen.
  3. Ausencia de filas idénticas repetidas dentro de un mismo anexo.
  4. Cierre por pliego contra el total impreso, cuando hay referencia.
"""
import csv, sys, json, itertools
from collections import defaultdict

BASE = 'Sí'          # valor de base_no_duplicada en las filas que suman

def cargar(ruta):
    with open(ruta, encoding='utf-8-sig') as fh:
        filas = list(csv.DictReader(fh, delimiter=';'))
    for f in filas:
        f['_m'] = int(f['monto_soles']) if f.get('monto_soles') not in ('', None) else None
    return filas

def control(filas, ref=None):
    fallas = []

    # 1. partición por nivel de gobierno
    pliegos = defaultdict(set)
    for f in filas:
        if f['base_no_duplicada'] == BASE and f['codigo_pliego']:
            pliegos[f['anexo']].add(f['codigo_pliego'])
    print('1. Partición de pliegos entre los anexos de la base')
    for a in sorted(pliegos):
        niveles = sorted({f['nivel_gobierno'] for f in filas if f['anexo'] == a})
        print(f'   anexo {a}: {len(pliegos[a]):>4} pliegos | {", ".join(niveles)}')
    for a, b in itertools.combinations(sorted(pliegos), 2):
        inter = pliegos[a] & pliegos[b]
        if inter:
            fallas.append(f'anexos {a} y {b} comparten {len(inter)} pliegos: {sorted(inter)[:5]}')
    print(f'   intersecciones: {"ninguna" if not fallas else "HAY SOLAPAMIENTO"}')

    # 2. contención de los cortes transversales
    print('\n2. Contención de los cortes transversales')
    base = defaultdict(int)
    for f in filas:
        if f['base_no_duplicada'] == BASE and f['_m'] is not None:
            base[f['codigo_pliego']] += f['_m']
    for anexo in sorted({f['anexo'] for f in filas if f['base_no_duplicada'] != BASE}):
        cruz = defaultdict(int)
        for f in filas:
            if f['anexo'] == anexo and f['_m'] is not None:
                cruz[f['codigo_pliego']] += f['_m']
        exc = [(c, v, base.get(c, 0)) for c, v in cruz.items() if v > base.get(c, 0)]
        print(f'   anexo {anexo}: {sum(cruz.values()):>15,} sobre una base de '
              f'{sum(base.get(c, 0) for c in cruz):>15,} | excesos: {len(exc)}')
        for c, v, b in exc[:5]:
            fallas.append(f'anexo {anexo}: el pliego {c} suma {v:,} sobre una base de {b:,}')

    # 3. filas idénticas repetidas
    print('\n3. Filas idénticas repetidas')
    k = defaultdict(int)
    for f in filas:
        k[(f['anexo'], f['codigo_pliego'], f['codigo_partida'], f['concepto'][:80],
           f.get('fuente_financiamiento', ''), f['monto_soles'])] += 1
    rep = sum(v - 1 for v in k.values() if v > 1)
    print(f'   duplicados exactos: {rep}')
    if rep:
        fallas.append(f'{rep} filas idénticas repetidas')

    # 4. cierre por pliego
    print('\n4. Cierre por pliego contra el total impreso')
    # Los pliegos nacionales aportan solo su porción territorial, no su
    # presupuesto completo: el archivo los marca como 'No aplica' y el
    # cierre no los alcanza.
    aplica = {f['codigo_pliego'] for f in filas
              if f.get('cuadra_el_pliego') not in ('No aplica', None, '')}
    if ref:
        # El total del anexo 4 se acepta solo si sus propias fuentes lo suman;
        # cuando el OCR dañó un dígito del total, manda la suma de fuentes.
        tot = {}
        for v in ref.values():
            if v['codigo'] in tot:
                continue
            tot[v['codigo']] = (v['total'] if sum(v['fuentes']) in (0, v['total'])
                                else sum(v['fuentes']))
        ok = mal = sin = 0
        for c, s in sorted(base.items()):
            if aplica and c not in aplica:
                continue
            if c not in tot:
                sin += 1
            elif tot[c] == s:
                ok += 1
            else:
                mal += 1
                print(f'   {c}: {s:>15,} vs {tot[c]:>15,}  dif {tot[c] - s:,}')
        print(f'   cuadran {ok} | no cuadran {mal} | sin referencia {sin}')
        if mal:
            fallas.append(f'{mal} pliegos no cuadran contra su total impreso')
    else:
        col = [f for f in filas if f.get('cuadra_el_pliego') == 'No']
        pl = {f['codigo_pliego'] for f in col}
        print(f'   pliegos marcados como no cuadrados en el archivo: {len(pl)}')
        if pl:
            fallas.append(f'{len(pl)} pliegos marcados con cuadre negativo')

    # partidas con importe ilegible
    ileg = [f for f in filas if f['_m'] is None]
    if ileg:
        print(f'\nAviso: {len(ileg)} partidas con importe ilegible en el PDF, '
              f'conservadas con el monto vacío')

    print('\n' + ('RESULTADO: sin observaciones' if not fallas else 'RESULTADO: observaciones'))
    for f in fallas:
        print('   - ' + f)
    return fallas

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    ref = None
    if '--ref' in sys.argv:
        ref = json.load(open(sys.argv[sys.argv.index('--ref') + 1]))
    sys.exit(1 if control(cargar(sys.argv[1]), ref) else 0)
