# Anime ids

Tabella ridotta che collega gli id TMDB agli id AniList e MyAnimeList, con stagione e scarto degli episodi.
Serve a trovare un anime per id nei siti che usano AniList e MyAnimeList, partendo da una serie o da un film di TMDB.

Il file `anime_ids.json` viene rigenerato ogni giorno da una GitHub Action a partire da
[Fribb/anime-lists](https://github.com/Fribb/anime-lists).

## Formato

```
{"v": 1,
 "tv":   {"<id serie TMDB>": [[stagione TMDB, id AniList, id MAL, scarto episodi, tipo], ...]},
 "film": {"<id film TMDB>":  [[id AniList, id MAL], ...]}}
```

Scarto episodi: numero da togliere all'episodio TMDB per avere l'episodio della scheda.
Esempio: stagione 3 con scarto 12, il 3x13 di TMDB e l'episodio 1 di quella scheda.

## Uso manuale

```
python3 genera.py
```
