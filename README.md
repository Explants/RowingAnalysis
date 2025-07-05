Rowing Technique Analysis using Computer Vision and Machine Learning
This project uses computer vision and machine learning to analyze rowing technique from video footage. The system extracts pose landmarks, calculates biomechanical metrics, and classifies rowing technique quality to help rowers and coaches improve performance.

Project Overview
The system processes rowing videos to:

Extract pose landmarks using MediaPipe
Calculate key biomechanical angles and distances
Classify rowing stages (Drive vs Recovery)
Rate technique quality based on common rowing faults
Features
Real-time Pose Detection: Uses MediaPipe to extract 33 pose landmarks from rowing videos
Biomechanical Analysis: Calculates knee angle, hip angle, elbow angle, and hand distance
Stroke Phase Classification: Automatically identifies Drive and Recovery phases
Technique Rating: Classifies technique using 11 common rowing faults:
Good Technique
Lean back too far
Lean forward too far
Pulling hands too early
Heels to wheels
Hands not close together
Dipping at the catch
Hanging at the catch
Hanging at the finish
Back swinging too early
Extending hands too early
Project Structure
rowing_vision/ ├── videos/ # Video files for analysis ├── landmarks.csv # Extracted pose landmarks ├── cleaned.csv # Processed biomechanical data ├── location_removal.py # Pose landmark extraction ├── data_cleaner.py # Data processing and feature engineering ├── training.py # Neural network training script └── training.ipynb # Jupyter notebook for model development

Installation
Prerequisites
Python 3.7+
CUDA-capable GPU (optional, for faster training)
Required Packages
pip install torch torchvision pip install mediapipe pip install opencv-python pip install pandas pip install numpy pip install scikit-learn pip install matplotlib pip install tensorflow # for keras preprocessing

Usage
1. Data Collection
Place rowing videos in the videos directory.

2. Pose Extraction
Run the pose detection script to extract landmarks: python location_removal.py

This will:

Process each video frame by frame
Extract pose landmarks using MediaPipe
Save coordinates to landmarks.csv
3. Data Processing
Process the raw landmarks into biomechanical features: python data_cleaner.py

This script:

Calculates joint angles and distances
Identifies stroke phases
Prompts for technique rating after each video
Saves processed data to cleaned.csv
4. Model Training
Train the neural network classifier: python training.py

Or use the Jupyter notebook training.ipynb for interactive development.

Technical Details
Pose Landmark Extraction
Uses MediaPipe Pose solution for real-time pose detection
Extracts 33 landmark points from each frame
Focuses on key points: shoulders, elbows, wrists, hips, knees, ankles
Feature Engineering
The system calculates several biomechanical metrics:

Knee Angle: Using law of cosines with ankle-knee-hip triangle knee_angle = math.degrees(math.acos(ratio))

Hip Angle: Torso lean angle relative to vertical hip_angle = math.degrees(math.atan(abs(shoulder[1] - hip[1]) / abs(shoulder[0] - hip[0])))

Hand Distance: Vertical separation between wrists hand_distance = abs(right_wrist[1] - left_wrist[1])

Stroke Phase Detection: Based on knee position changes over time

Neural Network Architecture
Input: 5 features (knee angle, hand distance, elbow angle, hip angle, stroke phase)
Hidden layers: 120 → 10 neurons
Output: 11 technique classifications
Loss function: CrossEntropyLoss
Optimizer: SGD with learning rate 0.001
Dataset Structure
Landmarks CSV
Contains frame-by-frame pose coordinates: iter,id,x,y 0,11,107,145 0,12,47,140 ...

Cleaned CSV
Processed biomechanical features: stage,knee_angle,hand_distance,hip_angle,elbow_angle,rating Drive,5.135,14.0,71.164,12.468, Recovery,4.398,14.0,68.710,26.284, ...

Model Performance
The current model uses a simple feedforward neural network. Future improvements could include:

LSTM networks for temporal sequence modeling
Larger datasets for better generalization
Transfer learning from sports biomechanics models
Real-time inference capabilities
Contributing
Fork the repository
Create a feature branch (git checkout -b feature/improvement)
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature/improvement)
Create a Pull Request
Future Enhancements
<input disabled="" type="checkbox"> Real-time video analysis
<input disabled="" type="checkbox"> Mobile app integration
<input disabled="" type="checkbox"> Additional biomechanical metrics
<input disabled="" type="checkbox"> Comparative analysis with elite rowers
<input disabled="" type="checkbox"> 3D pose estimation
<input disabled="" type="checkbox"> Automated video segmentation by stroke
License
This project is open source and available under the MIT License.

Acknowledgments
MediaPipe team for pose detection capabilities
Rowing coaching community for technique classification expertise
PyTorch team for deep learning framework
Contact
For questions or collaboration opportunities, please open an issue on GitHub.

Note: This project is for educational and research purposes. Professional rowing coaching should complement, not replace, computer vision analysis.
