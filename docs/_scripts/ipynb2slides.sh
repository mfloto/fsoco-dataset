#!/usr/bin/env bash

which jupyter >/dev/null || (echo "Couldn't find jupyter." && echo "Please make sure you've activated the correct virtual environment." && exit
1)

if [[ ! "$1" || "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Please input a valid path to a Jupyter Notebook to convert."
    echo ""
    echo "Usage: bash ipynb2slides.sh IPYNB_FILE"
    echo ""
    echo "Please note that the html output file will be written in the same"
    echo "directory as the input file. This behavior is due to how nbconvert works"
    exit 1
fi

stats_for_nerds_html=stats_for_nerds_bokeh.slides.html

jupyter nbconvert --to slides \
  --TemplateExporter.exclude_input=True \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_all_outputs_tags="{'hide_output'}" \
  --output hidden_input-analyse_stats \
  --stdout $1 > $stats_for_nerds_html 

# sed -i 's/Reveal\.initialize({/Reveal.initialize({width: "100%", height: "100%", margin: 0, minScale: 1, maxScale: 1,/' $stats_for_nerds_html

sed -i 's/Reveal\.initialize({/Reveal.initialize({width: 900, height: 900, margin: 0, minScale: 0.2, maxScale: 2.0,/' $stats_for_nerds_html

