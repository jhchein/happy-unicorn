# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import json
import time

import joblib
import pandas
import ptvsd  # For debugging / breakpoints
from azure.iot.device.aio import IoTHubModuleClient
from six.moves import input


def init():
    global model
    # this is a different behavior than before when the code is run locally, even though the code is the same.
    model_path = "model.pkl"
    # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)


ptvsd.enable_attach(("0.0.0.0", 5678))  # ADDED FOR DEBUGGING


async def main():
    ptvsd.break_into_debugger()  # ADDED FOR DEBUGGING

    try:
        print("IoT Hub Client for Python")

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        # define behavior for receiving an input message on input1
        async def input1_listener(module_client):
            while True:
                input_message = await module_client.receive_message_on_input(
                    "input1"
                )  # blocking call
                print("\n" * 3)
                print("the data in the message received on input1 was ")
                print(input_message.data)

                input_json = json.loads(input_message.data)
                input_df = pandas.DataFrame(
                    [
                        [
                            input_json["machine"]["temperature"],
                            input_json["machine"]["pressure"],
                            input_json["ambient"]["temperature"],
                            input_json["ambient"]["humidity"],
                        ]
                    ]
                )
                pred = model.predict(input_df)
                print("Prediction is ", pred[0])

                print("custom properties are")
                print(input_message.custom_properties)
                print("forwarding mesage to output1")
                await module_client.send_message_to_output(input_message, "output1")

        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    selection = input("Press Q to quit\n")
                    if selection == "Q" or selection == "q":
                        print("Quitting...")
                        break
                except:
                    time.sleep(10)

        # Schedule task for C2D Listener
        listeners = asyncio.gather(input1_listener(module_client))

        print("The sample is now waiting for messages. ")

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel listening
        listeners.cancel()

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print("Unexpected error %s " % e)
        raise


if __name__ == "__main__":
    init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())
