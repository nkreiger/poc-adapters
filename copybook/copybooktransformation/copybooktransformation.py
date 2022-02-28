from flask import Flask, request
from cloudevents.http import CloudEvent, to_binary, from_http, to_structured


import simplejson
import requests
import json
import os
from coboljsonifier.copybookextractor import CopybookExtractor
from coboljsonifier.parser import Parser
from coboljsonifier.config.parser_type_enum import ParseType

app = Flask(__name__)

bookfname='ASCII_BOOK.cob'

cb = os.environ.get('COPYBOOK')

text_file = open("ASCII_BOOK.cob", "x")
n = text_file.write(cb)
text_file.close()

dict_structure = CopybookExtractor(bookfname).dict_book_structure

parser = Parser(dict_structure, ParseType.FLAT_ASCII).build()
size = parser.size
print("// Registry calculated lenght:", size)
print("// " + "-" * 70)

# create an endpoint at http://localhost:/8080/
@app.route("/", methods=["POST"])
def home():
    # event = from_http(request.headers, request.get_data())
    message = json.loads(request.data.decode('utf-8'))
    x = message['data']

    parser.parse(x['data'])
    dictvalue = parser.value
    # print(simplejson.dumps(dictvalue))

    attributes = {
        "type": "com.example.sampletype1",
        "source": "https://example.com/event-producer",
    }

    data = simplejson.dumps(dictvalue)
    revent = CloudEvent(attributes, data)
    headers, body = to_binary(revent)
    sink = os.environ.get('K_SINK')
    print(headers['ce-type'])
    headers['ce-type'] = headers['ce-type'] + ".response"

    requests.post(sink, data=body, headers=headers)
    return "", 200

if __name__ == "__main__":
    app.run(port=8080)
