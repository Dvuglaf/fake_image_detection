An application with an interface for checking the authenticity of an image or face-image based on a deep learning.
METHODS were taken from open resources:

Method_ela_1 (PyTorch): consist of 2 part. First, it's check software signatures. Second, ela (error-level analysis).

Method_ela_2 (Keras): ela method built on a different model as opposed to the first method. 

Method_face_mobilenetv2 (Keras): method built on a MobileNetV2 model. Model was trained during 30 epochs, 
                         best val_accuracy = 0.9620 on 28 epoch.

Method_face_spoffnet (Keras): method built on a SpoffNet model. Bad accuracy, needs fine-tuning, but there was no dataset.

SETUP: need to add a directory 'models' to the project's root directory, then add models from disk to the directory, run 'interface.py'.


REFERENCES:
1) https://github.com/z1311/Image-Manipulation-Detection
2) https://www.kaggle.com/code/shaft49/real-vs-fake-images-casia-dataset
3) https://www.kaggle.com/code/anantgupt/real-vs-fake-faces/notebook#Accuracy-On-test-set
4) https://github.com/roytravel/pattern-recognition

MODELS: https://drive.google.com/drive/folders/1Lciwu3vetK88V8MWzVdLTy4BALPfMVUd

