echo "Create conda environment."
conda create -p ohd python==3.7 -y
echo "Conda environment created successfully."

echo "Activate conda environment."
conda activate ./ohd
echo "Environment Activated"

echo "Creating project structure."
mkdir .circleci .github docs notebooks src src/model src/static src/templates test
echo "Project structure created."

echo "started creating python script for each module.... :)"
touch .circleci/config.yaml
echo "circle-ci/config.yaml dir created successfully."

echo "started creating python script for each module."
touch .github/docs.yaml
echo ".github/docs.yaml file created successfully."

echo "started creating python script for each module."
mkdir src/model/brain_tumour_classification
mkdir src/model/Breast Cancer
mkdir src/model/Diabetes-Detection
mkdir src/model/Heart-Disease
mkdir src/model/Malaria-Detection
mkdir src/model/Pneumonia-Detection
mkdir src/model/thyroid-prediction-in-simple-ann
echo "src structure completed successfully"

echo "started creating python script for each module."
mkdir src/static/css
mkdir src/static/fonts
mkdir src/model/Diabetes-Detection
mkdir src/static/img
mkdir src/static/js
echo "src structure completed successfully"

echo "started creating python script for each module."
touch test/__init__.py
touch test/test.py
echo "src structure completed successfully"


