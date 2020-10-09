# coding: utf-8
from pathlib import Path

# import json
from collections import defaultdict
import os

# import shutil
# import click
# import cv2 as cv
# from multiprocessing import Pool
# import tqdm
# from functools import partial
import pascal_voc_writer

from supervisely_lib.io import fs as fs_utils
from supervisely_lib.imaging import image as image_utils
from supervisely_lib.project.project import Project, OpenMode
from supervisely_lib.annotation.annotation import Annotation
from supervisely_lib.geometry.rectangle import Rectangle

# from ..helpers import fsoco_to_class_id_mapping
# from watermark.watermark import FSOCO_IMPORT_BORDER_THICKNESS

OUT_IMG_EXT = ".jpg"
XML_EXT = ".xml"
TXT_EXT = ".txt"


def save_images_lists(path, tags_to_lists):
    for tag_name, samples_desc_list in tags_to_lists.items():
        with open(os.path.join(path, tag_name + TXT_EXT), "w") as fout:
            for record in samples_desc_list:
                fout.write(
                    "{}  {}\n".format(record[0], record[1])
                )  # 0 - sample name, 1 - objects count


def iterate_project(save_path: Path, project: Project):
    # Create root pascal 'datasets' folders
    for dataset in project.datasets:
        pascal_dataset_path = save_path / f"{dataset.name}"

        images_dir = pascal_dataset_path / "JPEGImages"
        anns_dir = pascal_dataset_path / "Annotations"
        lists_dir = pascal_dataset_path / "ImageSets" / "Layout"

        pascal_dataset_path.mkdir(exist_ok=True)
        images_dir.mkdir(exist_ok=True)
        anns_dir.mkdir(exist_ok=True)
        lists_dir.mkdir(exist_ok=True, parents=True)

        samples_by_tags = iterate_dataset(dataset, images_dir, anns_dir, project)
        save_images_lists(lists_dir, samples_by_tags)


def iterate_dataset(dataset, images_dir: Path, anns_dir: Path, project: Project):
    print(f"start export of {dataset}")
    samples_by_tags = defaultdict(list)  # TRAIN: [img_1, img2, ..]

    for item_name in dataset:
        print(f"exporting {item_name}")
        img_tags, no_ext_name, len_ann_labels = handle_image(
            item_name, dataset, images_dir, anns_dir, project
        )
        for tag in img_tags:
            samples_by_tags[tag.name].append((no_ext_name, len_ann_labels))

    return samples_by_tags


def handle_image(
    item_name, dataset, images_dir: Path, anns_dir: Path, project: Project
):
    img_path, ann_path = dataset.get_item_paths(item_name)
    no_ext_name = fs_utils.get_file_name(item_name)
    pascal_img_path = os.path.join(images_dir, no_ext_name + OUT_IMG_EXT)
    pascal_ann_path = os.path.join(anns_dir, no_ext_name + XML_EXT)

    if item_name.endswith(OUT_IMG_EXT):
        fs_utils.copy_file(img_path, pascal_img_path)
    else:
        img = image_utils.read(img_path)
        image_utils.write(pascal_img_path, img)

    ann = Annotation.load_json_file(ann_path, project_meta=project.meta)

    # Read tags for images lists generation
    # for tag in ann.img_tags:
    #     samples_by_tags[tag.name].append((no_ext_name, len(ann.labels)))

    writer = pascal_voc_writer.Writer(
        path=pascal_img_path, width=ann.img_size[1], height=ann.img_size[0]
    )

    for label in ann.labels:
        obj_class = label.obj_class
        rect: Rectangle = label.geometry.to_bbox()
        writer.addObject(
            name=obj_class.name,
            xmin=rect.left,
            ymin=rect.top,
            xmax=rect.right,
            ymax=rect.bottom,
        )
    writer.save(pascal_ann_path)

    return ann.img_tags, no_ext_name, len(ann.labels)


def main(sly_project_path: str, output_path: str, remove_watermark: bool):

    sly_project = Project(sly_project_path, OpenMode.READ)

    iterate_project(Path(output_path), sly_project)

    print(sly_project)
