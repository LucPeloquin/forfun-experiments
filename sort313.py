import os
import shutil
import numpy as np
import torch
from torchvision import models, transforms
from PIL import Image
from sklearn.cluster import KMeans

# ----------------------------
# User Settings – Update these paths and parameters as needed:
# ----------------------------
source_dir = 'path/to/your/images'      # Directory containing your images
dest_dir = 'path/to/sorted_images'        # Directory where sorted images will be stored
n_clusters = 5                           # Number of clusters to form

os.makedirs(dest_dir, exist_ok=True)

# ----------------------------
# Load a pre-trained ResNet50 model and modify it to output feature vectors.
# ----------------------------
# ResNet50 outputs a 2048-dimensional feature vector if we remove its classification head.
print("Loading ResNet50 model...")
model = models.resnet50(pretrained=True)
model.fc = torch.nn.Identity()  # Replace the final fully connected layer with an identity mapping
model.eval()  # Set the model to evaluation mode

# ----------------------------
# Define image preprocessing transforms.
# ResNet50 expects images resized and cropped to 224x224, and normalized with ImageNet statistics.
# ----------------------------
preprocess = transforms.Compose([
    transforms.Resize(256),              # Resize the shorter side to 256 pixels
    transforms.CenterCrop(224),          # Crop to 224x224
    transforms.ToTensor(),               # Convert the image to a PyTorch tensor
    transforms.Normalize(                # Normalize with mean and std as used in ImageNet
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ----------------------------
# Gather image file paths.
# ----------------------------
print("Collecting image files...")
valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
image_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir)
               if f.lower().endswith(valid_extensions)]

if not image_files:
    print("No images found in the source directory.")
    exit(1)

# ----------------------------
# Extract features from each image.
# ----------------------------
features = []
filenames = []

print("Extracting features from images...")
with torch.no_grad():  # Disable gradient computation for efficiency
    for file in image_files:
        try:
            # Open the image and ensure it's in RGB mode
            img = Image.open(file).convert("RGB")
            # Apply the preprocessing transforms
            input_tensor = preprocess(img)
            # Create a mini-batch as expected by the model
            input_batch = input_tensor.unsqueeze(0)
            # Extract features (output will have shape [1, 2048])
            output = model(input_batch)
            # Convert to a 1D numpy array
            feature = output.squeeze().numpy()
            features.append(feature)
            filenames.append(file)
        except Exception as e:
            print(f"Error processing {file}: {e}")

features = np.array(features)
print(f"Extracted features for {len(features)} images.")

# ----------------------------
# Cluster the images using K-Means.
# ----------------------------
print(f"Clustering images into {n_clusters} groups...")
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(features)

# ----------------------------
# Create subdirectories for each cluster and copy the images.
# ----------------------------
print("Copying images into cluster directories...")
for label in np.unique(labels):
    cluster_dir = os.path.join(dest_dir, f'cluster_{label}')
    os.makedirs(cluster_dir, exist_ok=True)

for file, label in zip(filenames, labels):
    dest_path = os.path.join(dest_dir, f'cluster_{label}', os.path.basename(file))
    shutil.copy(file, dest_path)

print("Done! Images have been sorted by visual similarity.")
