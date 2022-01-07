import json, argparse, os
from dataset_maker.image_downloader import retrieve_images
from dataset_maker.list_maker import make_list, create_new_subjects_train_val_list


def get_args():
    parser = argparse.ArgumentParser('Dataset maker')
    parser.add_argument('-s','--search_items',nargs='*', type=str, required=True, help='Search items')
    parser.add_argument('-n','--image_nr', type=int, help='Number of images per item to download')
    args = parser.parse_args()
    print('Search items:', args.search_items)
    print('Number of images per item:', args.image_nr)
    return args

def main():
    args = get_args()

    if os.path.exists('api_key_pexels.json'):    
        with open('api_key_pexels.json', 'r') as f:  # Json File with your API_KEY
            API_KEY = json.load(f)
    else:
        raise FileNotFoundError('Please create file [api_key_pexels.json] with your Pexels api key')


    # Download images
    querys_list = args.search_items # search terms
    nr_imgs = args.image_nr
    # querys_list = ['cats','dogs']  # search terms
    if nr_imgs is not None:
        retrieve_images(API_KEY ,querys_list, nr_imgs=nr_imgs)
    else:
        retrieve_images(API_KEY ,querys_list)



    # Make Lists
    list_name = f'{"_and_".join(querys_list)}_list'
    # list_name = 'cats_and_dogs_list'

    make_list(list_name=list_name, subjects=querys_list)
    create_new_subjects_train_val_list(filename=list_name)

    
if __name__ == '__main__':
    # get_args()
    main()
