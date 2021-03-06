import matplotlib.pyplot as plt
import pandas as pd
import cv2
from PIL import Image
from pathlib import Path

path = Path.home() / 'OneDrive - Seagroup/computer_vison/shopee_item_images/'
path_img = path / 'train_images'


def display_df(df, path, cols=6, rows=4):
    for k in range(rows):
        plt.figure(figsize=(20, 5))
        for j in range(cols):
            row = cols * k + j
            name = df['filepath'].tolist()[row]
            title = df['title'].tolist()[row]
            title_with_return = edit_title(title)

            img = cv2.imread(str(path / name))
            plt.subplot(1, cols, j + 1)
            plt.title(title_with_return)
            plt.axis('off')
            plt.imshow(img)
        plt.show()


def edit_title(text):
    title_with_return = ""
    for i, ch in enumerate(text):
        title_with_return += ch
        if (i != 0) & (i % 20 == 0):
            title_with_return += '\n'
    return title_with_return


def plot_image(df):
    img_path = df['filepath'].item()
    title = df['title'].item()
    title_with_return = edit_title(title)

    plt.figure(figsize=(20, 5))
    plt.title(title_with_return)
    img = cv2.imread(img_path)
    plt.imshow(img)
    plt.show()


def clean_text(text):
    return str(text).lower().strip()


def get_data(path, path_img):
    df = pd.read_csv(path)

    # clean
    df['filepath'] = df['image'].map(lambda x: str(path_img / x))
    group_dicts = df.groupby('label_group')["posting_id"].apply(set).apply(list).to_dict()
    df['target'] = df["label_group"].map(group_dicts)
    df['title_edit'] = df['title'].map(clean_text)
    return df


def show_images_horizontally(file):
    m = len(file) + 1
    fig, ax = plt.subplots(1, m)
    fig.set_figwidth(5 * m)

    for a, f in zip(ax, file):
        file_name, tit = f
        a.imshow(Image.open(file_name))
        title_with_return = edit_title(tit)
        a.title.set_text(title_with_return)
        a.axis("off")
    plt.show()


def show_image(file):
    file_name, tit = file
    fig, ax = plt.subplots(1, 1)
    title_with_return = edit_title(tit)

    fig.set_figwidth(5)
    ax.title.set_text(title_with_return)
    ax.imshow(Image.open(file_name))
    ax.axis("off")
