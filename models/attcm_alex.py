# import torch
# import torch.nn as nn
# import torch.nn.functional as F
 
# # =========================
# # Channel Attention
# # =========================
# class ChannelAttention(nn.Module):
#     def __init__(self, in_channels, reduction=16):
#         super(ChannelAttention, self).__init__()

#         self.fc1 = nn.Conv2d(in_channels, in_channels // reduction, 1)
#         self.fc2 = nn.Conv2d(in_channels // reduction, in_channels, 1)

#     def forward(self, x):
#         avg_pool = F.adaptive_avg_pool2d(x, 1)
#         max_pool = F.adaptive_max_pool2d(x, 1)

#         avg_out = self.fc2(F.relu(self.fc1(avg_pool)))
#         max_out = self.fc2(F.relu(self.fc1(max_pool)))

#         out = avg_out + max_out
#         return torch.sigmoid(out)


# # =========================
# # Spatial Attention
# # =========================
# class SpatialAttention(nn.Module):
#     def __init__(self):
#         super(SpatialAttention, self).__init__()

#         self.conv = nn.Conv2d(2, 1, kernel_size=7, padding=3)

#     def forward(self, x):
#         avg_out = torch.mean(x, dim=1, keepdim=True)
#         max_out, _ = torch.max(x, dim=1, keepdim=True)

#         x = torch.cat([avg_out, max_out], dim=1)
#         x = self.conv(x)

#         return torch.sigmoid(x)


# # =========================
# # AttCM Module
# # =========================
# class AttCM(nn.Module):
#     def __init__(self, channels):
#         super(AttCM, self).__init__()

#         self.ca = ChannelAttention(channels)
#         self.sa = SpatialAttention()

#     def forward(self, x):
#         x = x * self.ca(x)
#         x = x * self.sa(x)
#         return x


# # =========================
# # AttCM-AlexNet
# # =========================
# class AttCMAlexNet(nn.Module):
#     def __init__(self, num_classes=17):
#         super(AttCMAlexNet, self).__init__()

#         self.features = nn.Sequential(

#             nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
#             nn.ReLU(inplace=True),
#             nn.MaxPool2d(3, stride=2),

#             AttCM(64),

#             nn.Conv2d(64, 192, kernel_size=5, padding=2),
#             nn.ReLU(inplace=True),
#             nn.MaxPool2d(3, stride=2),

#             AttCM(192),

#             nn.Conv2d(192, 384, kernel_size=3, padding=1),
#             nn.ReLU(inplace=True),

#             nn.Conv2d(384, 256, kernel_size=3, padding=1),
#             nn.ReLU(inplace=True),

#             nn.Conv2d(256, 256, kernel_size=3, padding=1),
#             nn.ReLU(inplace=True),

#             nn.MaxPool2d(3, stride=2),
#         )

#         self.classifier = nn.Sequential(
#             nn.Dropout(),
#             nn.Linear(256 * 6 * 6, 4096),
#             nn.ReLU(inplace=True),

#             nn.Dropout(),
#             nn.Linear(4096, 4096),
#             nn.ReLU(inplace=True),

#             nn.Linear(4096, num_classes)
#         )

#     def forward(self, x):
#         x = self.features(x)
#         x = torch.flatten(x, 1)
#         x = self.classifier(x)
#         return x

import torch
import torch.nn as nn
import torch.nn.functional as F

# =========================
# Self-Attention (Lightweight)
# =========================
class SelfAttention(nn.Module):
    def __init__(self, in_dim):
        super(SelfAttention, self).__init__()

        self.query = nn.Conv2d(in_dim, in_dim // 8, 1)
        self.key   = nn.Conv2d(in_dim, in_dim // 8, 1)
        self.value = nn.Conv2d(in_dim, in_dim, 1)

        self.gamma = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        B, C, H, W = x.size()

        query = self.query(x).view(B, -1, H*W).permute(0, 2, 1)
        key   = self.key(x).view(B, -1, H*W)

        attention = torch.bmm(query, key)
        attention = F.softmax(attention, dim=-1)

        value = self.value(x).view(B, -1, H*W)

        out = torch.bmm(value, attention.permute(0, 2, 1))
        out = out.view(B, C, H, W)

        return self.gamma * out + x

# =========================
# Channel Attention
# =========================
class ChannelAttention(nn.Module):
    def __init__(self, in_channels, reduction=16):
        super(ChannelAttention, self).__init__()

        self.fc1 = nn.Conv2d(in_channels, in_channels // reduction, 1)
        self.fc2 = nn.Conv2d(in_channels // reduction, in_channels, 1)

    def forward(self, x):
        avg_pool = F.adaptive_avg_pool2d(x, 1)
        max_pool = F.adaptive_max_pool2d(x, 1)

        avg_out = self.fc2(F.relu(self.fc1(avg_pool)))
        max_out = self.fc2(F.relu(self.fc1(max_pool)))

        out = avg_out + max_out
        return torch.sigmoid(out)


# =========================
# Spatial Attention
# =========================
class SpatialAttention(nn.Module):
    def __init__(self):
        super(SpatialAttention, self).__init__()

        self.conv = nn.Conv2d(2, 1, kernel_size=7, padding=3)

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)

        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv(x)

        return torch.sigmoid(x)


# =========================
# AttCM Module (UPDATED with Residual)
# =========================
class AttCM(nn.Module):
    def __init__(self, channels):
        super(AttCM, self).__init__()

        self.ca = ChannelAttention(channels)
        self.sa = SpatialAttention()

    def forward(self, x):
        residual = x

        out = x * self.ca(x)
        out = out * self.sa(out)

        # Residual connection
        out = out + residual

        return out


# =========================
# AttCM-AlexNet (UPDATED)
# =========================
class AttCMAlexNet(nn.Module):
    def __init__(self, num_classes=17):
        super(AttCMAlexNet, self).__init__()

        self.features = nn.Sequential(

            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.BatchNorm2d(64),   # ← ADD THIS
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),

            AttCM(64),

            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.BatchNorm2d(192),   # ← ADD THIS
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),

            AttCM(192),

            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.BatchNorm2d(384),   # ← ADD THIS
            nn.ReLU(inplace=True),
            
            SelfAttention(384),

            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),   # ← ADD THIS
            nn.ReLU(inplace=True),

            SelfAttention(256),
            
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),   # ← ADD THIS
            nn.ReLU(inplace=True),

            nn.MaxPool2d(3, stride=2),
        )

        # 🔥 NEW: Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d((1, 1))

        # 🔥 UPDATED CLASSIFIER
        self.classifier = nn.Sequential(
            nn.Linear(256, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),

            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),

            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)

        # 🔥 Replace flatten with GAP
        x = self.gap(x)
        x = torch.flatten(x, 1)

        x = self.classifier(x)

        return x