/home/yassine/PFE/ML/.venv/bin/python /home/yassine/PFE/ML/script/data_preprocessing/clean_website.py
/home/yassine/PFE/ML/.venv/bin/python /home/yassine/PFE/ML/testing/prediction.py
echo sed -n '2p' predictions.csv | cut -d',' -f$(($(head -1 predictions.csv | tr -cd ',' | wc -c)+1-1)),$(($(head -1 predictions.csv | tr -cd ',' | wc -c)+1))
