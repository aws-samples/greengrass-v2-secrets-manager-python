# MIT No Attribution
#
# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import logging
import sys
from threading import Timer

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

TIMEOUT = 10

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def publish_secret():
    try:

        payload = {
            'SECRET_STRING': json_secret_string['SECRET_VALUE']
        }

        publish_operation = ipc_client.new_publish_to_iot_core()
        publish_operation.activate(
            request=model.PublishToIoTCoreRequest(topic_name='ggv2/secrets/demo',
                                                  qos='0',
                                                  payload=json.dumps(payload).encode()))

    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, publish_secret).start()


if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()

    # Retrieve secret
    get_secret_operation = ipc_client.new_get_secret_value()
    get_secret_operation.activate(request=model.GetSecretValueRequest(secret_id='greengrass_v2_secret'))
    secret_response = get_secret_operation.get_response().result()
    json_secret_string = json.loads(secret_response.secret_value.secret_string)
    get_secret_operation.close()

    # Start executing the function above
    publish_secret()
