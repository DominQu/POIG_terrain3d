# Projekt: Wizualizacja 3D danych 2D
Program tworzący mapę 3D z danych wysokości zawartych w różnego rodzaju plikach.

## Użytkowanie
W celu użycia programu należy zainstalować odpowiednie biblioteki języka Python.
Można zrobić to w następujący sposób:

Linux:

    pip install -r requirements.txt

Windows:

    pip install -r requirements-win.txt

Następnie w systemie Windows należy zainstalować moduł rasterio zgodnie z zaleceniami z dokumentacji tego modułu, dostępnymi na stronie https://rasterio.readthedocs.io/en/latest/installation.html

## Dane
Program zawiera dwie bitmapy wysokości:

- plik w formacie geotiff zawierający rzeczywiste dane elewacji ziemi zebrane podczas misji SRTM

- plik w formacie PNG zawierający bliżej nieokreślone miejsce na ziemi

Na wygenerowaną mapę nakładane są tekstury:

- na plik geotiff prawdziwe zdjęcia z satelity

- na plik PNG stworzone ręcznie w programie graficznym

Dane wysokości z misji SRTM pochodzą z projektu https://github.com/zhunor/threejs-dem-visualizer