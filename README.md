# Welcome to the repo for RWGQ8's MSc dissertation on pollinator monitoring at the Natural History Museum.

In this repo you will find folders containing code for the main steps in building the working software pipeline for the camera trap, and the dataset of observations captured in July-August 2026.

Most of the code was written by AI before being tested and checked manually.

## How to use the code

The code up to and including step 3 (YOLO training) assumes that you run the notebook in Colab, with a project folder in your connected Google Drive called `Colab Notebooks/Pollinator Camera Project`.
Some notebooks require subfolders to exist from previous steps.

Re-creating the entire workflow would require a little tinkering, as there were undocumented manual quality control and reorganisation steps involved. This was a proof of concept project so not everything was designed to be replicable.
Nevertheless, the available notebooks should show the main steps that I took. In particular, you can use it to see the exact hyperparameters and augmentations used in training the YOLO v11 model, and to explore the dataset of image crops that the camera captured.
