# Install necessary packages for I2C communication
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools

# Check if AMG8833 is able to communicate with Raspberry Pi
sudo i2cdetect -y 1

# Set the I2C clock frequency at 400kHz for AMG8833 communication
sudo nano /boot/config.txt

# Add the following lines to the file and save it
dtparam=i2c_arm=on, i2c_arm_baudrate=400000

# Install required libraries and dependencies for AMG8833
sudo apt-get update
sudo apt-get install -y build-essential python-pip python-dev python-smbus git

# Clone Adafruit_Python_GPIO repository and install
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install

# Install pygame and scipy
sudo apt-get install -y python-scipy python-pygame
sudo pip install colour Adafruit_AMG88xx

# Clone the Adafruit_AMG88xx_python repository
cd ~/
git clone https://github.com/adafruit/Adafruit_AMG88xx_python

# Navigate to the examples directory
cd Adafruit_AMG88xx_python/examples

# Run the example script
sudo python thermal_cam.py
