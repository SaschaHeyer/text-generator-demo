from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO
import json

from fastai import *
from fastai.text import *

model_en_url = 'https://www.dropbox.com/s/ct01m9qvivhdwpb/english.pkl?raw=1'
model_es_url = 'https://www.dropbox.com/s/kgjdlqmjgtwsoxd/spanish.pkl?raw=1'

model_en_name = 'english.pkl'
model_es_name = 'spanish.pkl'

path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_en_url, path/'models'/f'{model_en_name}')
    await download_file(model_es_url, path/'models'/f'{model_es_name}')

    learn_en = load_learner(path/'models', fname=model_en_name)
    learn_es = load_learner(path/'models', fname=model_es_name)
    return learn_en,learn_es

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn_en, learn_es = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    data = await request.form()
    init_text = data['text']
    language = data['language']
    #img_bytes = await (data['file'].read())
    #img = open_image(BytesIO(img_bytes))
    #return JSONResponse({'result': learn.predict(img)[0]})
    n_words = 200
    n_sentences = 1
    out = ''
    if (language == 'en'):
        out = learn_en.predict(init_text, n_words, temperature=0.75)
    elif (language == 'es'):
        out = learn_es.predict(init_text, n_words, temperature=0.75)
    return JSONResponse({'result': json.dumps(out)})

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app, host='0.0.0.0', port=80)

