import torch
import torchvision.models as models
import torch.nn as nn

def load_model(model_path):
    model = models.resnet50(weights=None)
    num_ftrs = model.fc.in_features
    
    num_classes = 11
    model.fc = nn.Linear(num_ftrs, num_classes)

    checkpoint = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)

    model.load_state_dict(checkpoint)

    return model
