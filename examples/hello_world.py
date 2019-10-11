from flask import Flask, request
from fbmsg import FacebookClient, messages

app = Flask(__name__)
client = FacebookClient('TOKEN')


@client.register_text_message_processor()
def text_handler(incoming):
    msg = messages.Message(incoming.text)
    client.send_message(incoming.sender_id, msg)


@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
    if request.json:
        client.process_json(request.json)
    try:
        return request.args['hub.challenge']
    except:
        return ''

app.run()