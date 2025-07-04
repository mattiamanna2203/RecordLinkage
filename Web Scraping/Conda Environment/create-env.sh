#!/bin/bash
cd ".../Conda Environment" # Path della cartella over il file setup-env.yml è collocato
conda env create -f setup-env.yml -n scraper # Per creare un conda environment adatto al web scraping, i pacchetti necessari sono inseriti nel file 'setup-env.yml'