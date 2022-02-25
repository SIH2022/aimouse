import configparser
config = configparser.ConfigParser()
config['train'] = {}
config['test'] = {}

# path to store log files
config['train']['log'] ='/home/vikasjoshis001/Desktop/FaceRecognition/logs'

# store images in this folder
config['train']['images_to_train'] = '/home/vikasjoshis001/Desktop/FaceRecognition/images_to_train'

#trained images will be transfered to this folder
config['train']['trained_images'] = '/home/vikasjoshis001/Desktop/FaceRecognition/trained_images'

#detected images will be stored here as a log
config['test']['save_images'] = '/home/vikasjoshis001/Desktop/FaceRecognition/logs/images'

with open('config.ini', 'w') as configfile:
  config.write(configfile)
