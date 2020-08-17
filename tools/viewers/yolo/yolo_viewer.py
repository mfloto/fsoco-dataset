#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import math
import cv2
from random import shuffle
from screeninfo import get_monitors

ID_TO_COLOR = {
    "0": (0, 255, 255),
    "1": (255, 0, 0),
    "2": (0, 255, 0),
    "3": (0, 165, 255),
    "4": (0, 100, 255),
    "5": (0, 0, 0),
}

LABEL_FILE_EXTENSION = ".txt"
IMAGES_SUBDIR = "images"
LABELS_SUBDIR = "labels"

CV_FONT = cv2.FONT_HERSHEY_SIMPLEX

HEIGHT_MARGIN = 130
WIDTH_MARGIN = 20

screen_width = 0
screen_height = 0


def handle_folder(folder: Path, sample_size: float):
    images_directory = folder / IMAGES_SUBDIR
    labels_directory = folder / LABELS_SUBDIR

    if images_directory.exists() and labels_directory.exists():
        label_files = list(labels_directory.glob("*{}".format(LABEL_FILE_EXTENSION)))

        if len(label_files) == 0:
            print(f"{labels_directory} does not contain any label files!")
            return False

        shuffle(label_files)
        num_samples = math.ceil(len(label_files) * sample_size)
        samples = sorted(label_files[:num_samples])

        index = 0
        while True:
            image_file = images_directory / samples[index].stem
            action = handle_image(samples[index], image_file, index, num_samples)

            if action == "next":
                index += 1
                if index >= num_samples:
                    index = 0

            elif action == "previous":
                index -= 1
                if index < 0:
                    index = num_samples - 1

            elif action == "quit":
                break

    else:
        print(f"{folder} does not contain a labels or images directory!")


def handle_image(label_file: Path, image_file: Path, index: int, total: int):
    image = cv2.imread(str(image_file))
    image_width = image.shape[1]
    image_height = image.shape[0]

    with open(label_file, "r") as label_file:

        for line in label_file:
            data = line.split(" ")
            class_id = data[0]
            norm_x, norm_y, norm_bb_width, norm_bb_height = [float(f) for f in data[1:]]

            color = ID_TO_COLOR[str(class_id)]

            x = int((norm_x - norm_bb_width / 2) * image_width)
            y = int((norm_y - norm_bb_height / 2) * image_height)
            w = int(norm_bb_width * image_width)
            h = int(norm_bb_height * image_height)

            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

    # rescale to fit screen

    ratio = image_width / image_height

    new_width = int(screen_width)
    new_height = int(screen_width / ratio)

    if new_height > screen_height:
        new_width = int(screen_height * ratio)
        new_height = int(screen_height)

    image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # and info

    overlay = image.copy()
    x, y, w, h = 0, 0, new_width, 80
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (20, 20, 20), -1)
    alpha = 0.8
    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    cv2.putText(
        image,
        f"press 'n' for next | 'p' for previous | 'q' for quit",
        (20, 30),
        CV_FONT,
        1.0,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        image,
        f"[{index + 1}/{total}] {image_file}",
        (20, 70),
        CV_FONT,
        1.0,
        (255, 255, 255),
        2,
    )

    cv2.imshow("image", image)

    action = ""
    while True:
        key = cv2.waitKey(1)
        if key == ord("n"):
            action = "next"
            break
        elif key == ord("p"):
            action = "previous"
            break
        elif key == ord("q"):
            action = "quit"
            break

    return action


def get_screen_size():
    global screen_width, screen_height
    for m in get_monitors():
        if m.width > screen_width and m.height > screen_height:
            screen_width = m.width - WIDTH_MARGIN
            screen_height = m.height - HEIGHT_MARGIN


def main(input_folders: list, sample_size: float):
    get_screen_size()

    for folder in input_folders:
        handle_folder(Path(folder), sample_size=sample_size)
