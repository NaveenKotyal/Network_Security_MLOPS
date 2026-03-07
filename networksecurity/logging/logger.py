import logging
import os
from datetime import datetime

# Step 1: Create log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Step 2: Create logs folder
logs_folder = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_folder, exist_ok=True)

# Step 3: Full file path
LOG_FILE_PATH = os.path.join(logs_folder, LOG_FILE)

# Step 4: Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH), # Writes to file
        logging.StreamHandler()              # Prints to console
    ]
)

