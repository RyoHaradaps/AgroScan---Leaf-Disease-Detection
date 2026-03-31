import torch
from torchvision import transforms
from PIL import Image

from models.attcm_alex import AttCMAlexNet
from utils.classes import CLASS_NAMES

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
model = AttCMAlexNet(num_classes=len(CLASS_NAMES))
model.load_state_dict(torch.load("checkpoints/final~/agroscan_v1.pth", map_location=device, weights_only=True))
model.to(device)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_image(image: Image.Image):
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1)
        confidence, pred = torch.max(probs, 1)

    return CLASS_NAMES[pred.item()], confidence.item()