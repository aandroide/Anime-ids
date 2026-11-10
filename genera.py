# -*- coding: utf-8 -*-
# Genera anime_ids.json: tabella ridotta da id TMDB a id AniList e MyAnimeList.
# Fonte: https://github.com/Fribb/anime-lists (anime-list-full.json).
#
# Formato del file generato:
#   {"v": 1,
#    "tv":   {"<id serie TMDB>": [[stagione TMDB, id AniList, id MAL, scarto episodi, tipo], ...]},
#    "film": {"<id film TMDB>":  [[id AniList, id MAL], ...]}}
# scarto episodi: numero da togliere all'episodio TMDB per avere l'episodio della scheda
#   (esempio: stagione 3, scarto 12: il 3x13 di TMDB e l'episodio 1 di quella scheda).
# Valori mancanti: null.
#
# Uso: python3 genera.py [file sorgente locale]   (senza argomenti scarica la fonte)

import json
import sys
import urllib.request

FONTE = 'https://raw.githubusercontent.com/Fribb/anime-lists/master/anime-list-full.json'
USCITA = 'anime_ids.json'
MINIMO_SERIE = 3000   # sotto questa soglia la fonte e considerata rotta e il file non viene toccato


def _leggi(percorso=None):
    if percorso:
        with open(percorso, encoding='utf-8') as f:
            return json.load(f)
    with urllib.request.urlopen(FONTE, timeout=120) as r:
        return json.loads(r.read().decode('utf-8'))


def _numero(valore, chiave='tmdb'):
    if isinstance(valore, dict):
        valore = valore.get(chiave)
    return valore if isinstance(valore, int) else None


def genera(voci):
    tv, film = {}, {}
    for x in voci:
        anilist, mal = x.get('anilist_id'), x.get('mal_id')
        if not anilist and not mal:
            continue
        tmdb = x.get('themoviedb_id')
        if not isinstance(tmdb, dict):
            continue
        serie = tmdb.get('tv')
        if isinstance(serie, int):
            tv.setdefault(str(serie), []).append(
                [_numero(x.get('season')), anilist or None, mal or None, _numero(x.get('episode_offset')) or 0,
                 x.get('type') or ''])
        titoli = tmdb.get('movie')
        if isinstance(titoli, int):
            titoli = [titoli]
        for t in titoli or []:
            if isinstance(t, int):
                film.setdefault(str(t), []).append([anilist or None, mal or None])
    for elenco in tv.values():
        elenco.sort(key=lambda r: (r[0] if r[0] is not None else 999, r[3], r[1] or 0))
    for elenco in film.values():
        elenco.sort(key=lambda r: (r[0] or 0, r[1] or 0))
    return {'v': 1,
            'tv': dict(sorted(tv.items(), key=lambda c: int(c[0]))),
            'film': dict(sorted(film.items(), key=lambda c: int(c[0])))}


def main():
    voci = _leggi(sys.argv[1] if len(sys.argv) > 1 else None)
    tabella = genera(voci)
    if len(tabella['tv']) < MINIMO_SERIE:
        print('Fonte incompleta: solo %d serie, file non aggiornato' % len(tabella['tv']))
        return 1
    with open(USCITA, 'w', encoding='utf-8') as f:
        json.dump(tabella, f, separators=(',', ':'))
        f.write('\n')
    print('Serie: %d, film: %d' % (len(tabella['tv']), len(tabella['film'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
