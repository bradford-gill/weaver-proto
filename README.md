# weaver-proto
use AI to create lesson plans

## Docker deployment
~~~bash
docker build -t proto .

# if .env file does not exist -> nano .env
docker run -d --env-file .env -p 80:80 proto
~~~

## Local Deployment
~~~bash
# (if needed) install uv 
curl -LsSf https://astral.sh/uv/install.sh | sh

# go to chatbot dir and create env
cd chatbot
uv venv .venv

# activate venv
source .venv/bin/activate

# install requirements
uv pip install -r requirements.txt

streamlit run main.py
~~~