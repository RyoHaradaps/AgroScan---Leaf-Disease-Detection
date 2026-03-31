# import torch
# import torch.nn as nn
# import torch.optim as optim
# from sklearn.metrics import classification_report
# from collections import Counter

# from models.attcm_alex import AttCMAlexNet
# from utils.dataset import get_dataloaders
# import torch.nn.functional as F

# class FocalLoss(nn.Module):
#     def __init__(self, alpha=1.5, gamma=2):
#         super().__init__()
#         self.alpha = alpha
#         self.gamma = gamma

#     def forward(self, inputs, targets):
#         ce_loss = F.cross_entropy(inputs, targets, reduction='none')
#         pt = torch.exp(-ce_loss)
#         loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
#         return loss.mean()

# # =========================
# # CONFIG
# # =========================
# DATA_DIR = "data/AgroScan_Split"
# BATCH_SIZE = 32
# EPOCHS = 30
# LR = 0.0003


# # =========================
# # DEVICE
# # =========================
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)


# # =========================
# # DATA
# # =========================
# train_loader, val_loader, test_loader, class_names, num_classes = get_dataloaders(DATA_DIR, BATCH_SIZE)


# # =========================
# # CLASS WEIGHTS (IMPORTANT)
# # =========================
# targets = train_loader.dataset.targets
# class_counts = Counter(targets)

# total_samples = len(targets)
# num_classes = len(class_counts)

# # weights = [total_samples / class_counts[i] for i in range(num_classes)]
# # weights = torch.tensor(weights, dtype=torch.float).to(device)


# # =========================
# # MODEL
# # =========================
# model = AttCMAlexNet(num_classes=num_classes).to(device)


# # =========================
# # LOSS + OPTIMIZER
# # =========================
# criterion = FocalLoss()
# optimizer = optim.Adam(model.parameters(), lr=LR)

# scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.3)


# # =========================
# # TRAINING LOOP
# # =========================
# for epoch in range(EPOCHS):

#     model.train()
#     running_loss = 0

#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device)

#         optimizer.zero_grad()
#         outputs = model(images)
#         loss = criterion(outputs, labels)

#         loss.backward()
#         optimizer.step()

#         running_loss += loss.item() * images.size(0)

#     scheduler.step()

#     epoch_loss = running_loss / len(train_loader.dataset)
#     print(f"Epoch [{epoch+1}/{EPOCHS}] Loss: {epoch_loss:.4f}")


# # =========================
# # VALIDATION
# # =========================
# model.eval()

# all_preds = []
# all_labels = []

# with torch.no_grad():
#     for images, labels in val_loader:
#         images = images.to(device)

#         outputs = model(images)
#         preds = torch.argmax(outputs, dim=1).cpu().numpy()

#         all_preds.extend(preds)
#         all_labels.extend(labels.numpy())

# print("\nVALIDATION REPORT:\n")
# print(classification_report(all_labels, all_preds, target_names=class_names))


# # =========================
# # TEST EVALUATION
# # =========================
# all_preds = []
# all_labels = []

# with torch.no_grad():
#     for images, labels in test_loader:
#         images = images.to(device)

#         outputs = model(images)
#         preds = torch.argmax(outputs, dim=1).cpu().numpy()

#         all_preds.extend(preds)
#         all_labels.extend(labels.numpy())

# print("\nTEST SET REPORT:\n")
# print(classification_report(all_labels, all_preds, target_names=class_names))


# # =========================
# # SAVE MODEL
# # =========================
# torch.save(model.state_dict(), "checkpoints/attcm_alex.pth")
# print("\nModel saved successfully!")
import torch    # After removing Rice healthy
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import classification_report
from collections import Counter

from models.attcm_alex import AttCMAlexNet
from utils.dataset import get_dataloaders
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=1.5, gamma=2):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        return loss.mean()

# =========================
# CONFIG
# =========================
DATA_DIR = "data/AgroScan_Split"
BATCH_SIZE = 32
EPOCHS = 30
LR = 0.0003


# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


# =========================
# DATA
# =========================
train_loader, val_loader, test_loader, class_names, num_classes = get_dataloaders(DATA_DIR, BATCH_SIZE)


# =========================
# CLASS WEIGHTS (IMPORTANT)
# =========================
targets = train_loader.dataset.targets
class_counts = Counter(targets)

total_samples = len(targets)
num_classes = len(class_counts)

# weights = [total_samples / class_counts[i] for i in range(num_classes)]
# weights = torch.tensor(weights, dtype=torch.float).to(device)


# =========================
# MODEL
# =========================
model = AttCMAlexNet(num_classes=num_classes).to(device)


# =========================
# LOSS + OPTIMIZER
# =========================
criterion = FocalLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.3)


# =========================
# TRAINING LOOP
# =========================
for epoch in range(EPOCHS):

    model.train()
    running_loss = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

    scheduler.step()

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f"Epoch [{epoch+1}/{EPOCHS}] Loss: {epoch_loss:.4f}")


# =========================
# VALIDATION
# =========================
model.eval()

all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in val_loader:
        images = images.to(device)

        outputs = model(images)
        preds = torch.argmax(outputs, dim=1).cpu().numpy()

        all_preds.extend(preds)
        all_labels.extend(labels.numpy())

print("\nVALIDATION REPORT:\n")
print(classification_report(all_labels, all_preds, target_names=class_names))


# =========================
# TEST EVALUATION
# =========================
all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)

        outputs = model(images)
        preds = torch.argmax(outputs, dim=1).cpu().numpy()

        all_preds.extend(preds)
        all_labels.extend(labels.numpy())

print("\nTEST SET REPORT:\n")
print(classification_report(all_labels, all_preds, target_names=class_names))


# =========================
# SAVE MODEL
# =========================
torch.save(model.state_dict(), "checkpoints/attcm_alex.pth")
print("\nModel saved successfully!")