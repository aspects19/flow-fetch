# FastFlow
FastFlow is a **FastAPI** fullstack video downloader app.

![Python](https://img.shields.io/badge/v3.12.9-blue?style=flat&logo=python&logoColor=yellow&label=python&color=yellow)
![FastAPI](https://img.shields.io/badge/v0.115.10-009485?style=flat&logo=fastapi&logoColor=white&label=fastapi&color=009485)
![Jinja2](https://img.shields.io/badge/v3.1.5-b41717?style=flat&logo=jinja&logoColor=white&label=jinja2&color=b41717)
![PostgreSQL](https://img.shields.io/badge/v2.9.10-31648C?style=flat&logo=postgresql&logoColor=white&label=psycopg2&color=31648C)

# Features

- [x] Download videos from hundreds of websites with ability to choose resolutions
- [x] Visual appealing UI.
- [ ] Download Music.
- [ ] Power a Telegram BOT.
- [ ] Implement premium features.

# Installation

To run the Weather App locally, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/aspects19/flow-fetch.git
   ```

2. Navigate into the project directory:

   ```sh
   cd flow-fetch
   ```
3 . Create a python virtual environment and install project dependendencies

``` sh
# For Linux/Mac
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

```

*or*

```sh
# For Windows
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

4.Rename ***.env.example*** to ***.env*** and replace it with your postgresql credentials <u>**example** </u>

```sh
DB_URL = "postgresql+psycopg2://postgres:test_123#@localhost:5432/flowfetch"

```
5. Run the app using

```sh
python main.py
```

🎉 Your app is live, you can now access it through the given endpoint
