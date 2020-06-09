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
# post_markup += '<figure><img src="https://images.pexels.com/photos/3985158/pexels-photo-3985158.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260"/><figcaption>По всем вопросам: freedaba@protonmail.com</figcaption></figure>'
# post_markup += '<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.kYri6tUHsUdvXAl68j7CrQHaFj%26pid%3DApi&f=1"/>'
post_markup += '<img src="https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"/>'
# post_markup += '<img src="https://images.unsplash.com/photo-1519494080410-f9aa76cb4283?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1353&q=80"/>'

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


