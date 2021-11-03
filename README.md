# Deploy an ML Model on IoT Edge using VS Code and 'Azure IoT Edge' Extension

This is a demo how to deploy your own Machine Learning model as an IoT Edge Module.

## Getting started

Most of the code in this repostitory was automatically created as an IoT Edge Solution with the "Azure IoT Edge" extension.

The easiest way to make use of this repo is to install the Azure IoT Edge extension, create your own iot edge solution and adjust your Module in a similar fashion as I did and according to your model and preprocessing.

Essentially you want to

* add your model (e.g. pickle file)
* update requirement.txt with all required packages 
* update your main.py
  * load the model in init()
  * update input1_listener to accomodate to your request schema
* Build your solution and or a specific Module image (e.g. only your arm32 image) using the IoT Edge extension
  * Don't forget to update your module.json (image/tag/version) each time you update your code ... so that your IoT Edge Device understands there is a new version to be fetched from your Container Registry.
