# -*- coding: utf-8 -*-

import asyncio
from telegraph import Telegraph
from database import AioSQL as sqlite


telegraph = Telegraph()

r = telegraph.create_account(short_name='MS-Bot')

print(r)

loop = asyncio.get_event_loop()
all_msc = loop.run_until_complete(sqlite.get_all_msc())

post_markup = "<h4>Открытая база медицинских центров, занимающихся вопросами Рассеянного склероза.</h4>"
post_markup += '<img src="https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"/>'

for msc in all_msc:
    new_paragraph = ", <br>".join(msc[1:4])
    post_markup += f"<p>🔸 {new_paragraph}</p>"

response = telegraph.create_page(
    title="Список РС-Центров 👨‍⚕️",
    html_content=post_markup,
    author_name='MS-Bot',
)
print(response['url'])
print(f'https://tgraph.io/{response["path"]}')


