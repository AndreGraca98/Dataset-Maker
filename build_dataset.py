import json
from dataset_maker.image_downloader import retrieve_images
from dataset_maker.list_maker import make_list, create_new_subjects_train_val_list


with open('api_key_pexels.json', 'r') as f:  # Json File with your API_KEY
    API_KEY = json.load(f)


querys_list = ['cats','dogs']  # search terms
retrieve_images(API_KEY ,querys_list)



list_name = 'cats_and_dogs_list'
make_list(list_name=list_name, subjects=['cats', 'dogs'])
create_new_subjects_train_val_list(filename=list_name)


