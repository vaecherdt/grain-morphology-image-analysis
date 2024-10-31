import torch
from torchvision import transforms
from PIL import Image, UnidentifiedImageError

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def preprocess_image(image_path):
    try:
        image = Image.open(image_path)
        image = preprocess(image)
        return image.unsqueeze(0)
    except UnidentifiedImageError:
        print(f"Erro: O arquivo '{image_path}' não é uma imagem válida.")
        return None
    except Exception as e:
        print(f"Erro ao processar a imagem '{image_path}': {e}")
        return None

def predict_image(image_path, model):
    image_tensor = preprocess_image(image_path)
    
    if image_tensor is None:
        return None

    try:
        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted = torch.max(outputs, 1)
        return predicted.item()
    except Exception as e:
        print(f"Erro ao fazer a predição para a imagem '{image_path}': {e}")
        return None
