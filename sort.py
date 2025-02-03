import os
import shutil
import numpy as np

from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.cluster import KMeans

# ----------------------------
# User Settings – Update these paths and parameters as needed:
# ----------------------------
source_dir = 'path/to/your/images'      # directory containing your images
dest_dir = 'path/to/sorted_images'        # directory where sorted images will be stored
n_clusters = 5                           # number of clusters you want to form
image_size = (224, 224)                  # VGG16 expects 224x224 images

# Create destination directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

# ----------------------------
# Load pre-trained VGG16 model with global average pooling to get a flat feature vector.
# ----------------------------
print("Loading VGG16 model...")
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

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
# Extract features for each image.
# ----------------------------
features = []
filenames = []

print("Extracting features from images...")
for file in image_files:
    try:
        # Load and resize image
        img = image.load_img(file, target_size=image_size)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        # Preprocess image for VGG16
        x = preprocess_input(x)
        # Extract features
        feat = model.predict(x)
        features.append(feat.flatten())
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
for label in set(labels):
    cluster_dir = os.path.join(dest_dir, f'cluster_{label}')
    os.makedirs(cluster_dir, exist_ok=True)

for file, label in zip(filenames, labels):
    dest_path = os.path.join(dest_dir, f'cluster_{label}', os.path.basename(file))
    shutil.copy(file, dest_path)

print("Done! Images have been sorted by visual similarity.")
