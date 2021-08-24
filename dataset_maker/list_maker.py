import os, time, datetime, json, tqdm, glob
from typing import Dict, List
import pandas as pd


tqprint = tqdm.tqdm.write


def make_list(list_name: str = 'main_list', subjects: List[str] = None):

    available_classes = sorted(os.listdir('data'))
    classes = available_classes if not subjects else list(filter((lambda s: s in available_classes), subjects))

    
    classes2number = {clss:i for i, clss in enumerate(classes)}    
    with open(f'lists/{list_name}_classes2numbers.json', 'w') as f:
        json.dump(classes2number, f)

    if subjects:
        available_paths = []
        for s in subjects:
            available_paths.extend(sorted(glob.glob(f'data/{s}/*')) )
    else:
        available_paths = sorted(glob.glob('data/*/*'))
    
    paths = [path for path in available_paths if 'urls.json' not in path]

    data = []
    for pth in (paths):
        clss = [v for k, v in classes2number.items() if k in pth]
        data.append([pth, clss[0]])

    df = pd.DataFrame(data, columns=['img_path', 'label'])
    df.to_csv(f'lists/{list_name}.txt', sep=',', index=None)


def shuffle_df(df, n_pics=10):
    df_list = [ ]
    for i in range(0, df.shape[0], n_pics):
        aux_df = df[ i:i + n_pics ].sample(frac=1).reset_index(drop=True)
        df_list.append(aux_df)

    
    shuffled_df = pd.concat(df_list)
    # print(shuffled_df)

    # # # shuffled_df.to_csv('lists/shuffled.txt', index=None)
    
    return shuffled_df


def shuffle_split_df(df, n_pics=10):
    df1_list = [ ]
    df2_list = [ ]
    split_len = int(n_pics * .8)

    for i in range(0, df.shape[0], n_pics):
        aux_df = df[ i:i + n_pics ].sample(frac=1).reset_index(drop=True)
        df1, df2 = aux_df[:split_len], aux_df[split_len:]

        df1_list.append(df1)
        df2_list.append(df2)

    
    shuffled_df1 = pd.concat(df1_list)
    shuffled_df2 = pd.concat(df2_list)


    return shuffled_df1, shuffled_df2


def create_new_subjects_train_val_list(filename='main_list'):

    read_df = pd.read_csv(f'lists/{filename}.txt')    

    df = shuffle_df(read_df)

    train, val = shuffle_split_df(df)


    train.to_csv(f'lists/{filename}_train.txt', index=None, sep=',')
    val.to_csv(f'lists/{filename}_val.txt', index=None, sep=',')
    

# list_name = 'cats_and_dogs_list'
# make_list(list_name=list_name, subjects=['cats', 'dogs'])
# create_new_subjects_train_val_list(filename=list_name)

