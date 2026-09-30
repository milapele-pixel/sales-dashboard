# Sales Performance Dashboard

Streamlit versija, kas sagatavota publicēšanai Streamlit Community Cloud.

## Projekta faili

- `streamlit_app.py` — dashboard aplikācija.
- `sales_data_capstone.csv` — dashboard dati.
- `requirements.txt` — Python bibliotēkas, ko Streamlit Cloud instalēs automātiski.

## Palaišana lokāli

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Datu atjaunošana

Pēc `sales_data_capstone.csv` atjaunināšanas GitHub repozitorijā Streamlit Cloud
pārpublicē aplikāciju. Dati tiek kešoti 10 sekundes. Aplikācijā ir arī poga
`🔄 Pārlādēt datus`, kas iztīra datu kešatmiņu un pārrēķina KPI.

## Publicēšana Streamlit Community Cloud

1. Izveido GitHub repozitoriju.
2. Augšupielādē visus projekta failus repozitorija saknes mapē.
3. Atver https://share.streamlit.io un pieslēdzies ar GitHub.
4. Izvēlies `Create app` un pēc tam `Yup, I have an app`.
5. Norādi GitHub repozitoriju, zaru `main` un galveno failu `streamlit_app.py`.
6. Nospied `Deploy`.

Pēc publicēšanas tiks izveidota pastāvīga `streamlit.app` saite.
