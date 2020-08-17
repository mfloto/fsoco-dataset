from pathlib import Path
import json
from collections import defaultdict
import os
import shutil
import click

from ..helpers import fsoco_classes

# Class counter
class_counter = defaultdict(int)


def clean_export_dir(darknet_export_images_dir: Path, darknet_export_labels_dir: Path):
    shutil.rmtree(darknet_export_images_dir, ignore_errors=True)
    shutil.rmtree(darknet_export_labels_dir, ignore_errors=True)
    darknet_export_images_dir.mkdir(parents=True)
    darknet_export_labels_dir.mkdir(parents=True)


def export_image(darknet_export_images_dir: Path, src_file: Path, new_file_name: str):
    old_file_name = src_file.name
    dst_dir = darknet_export_images_dir
    shutil.copy(str(src_file), dst_dir)

    dst_file = os.path.join(dst_dir, old_file_name)
    new_dst_file_name = os.path.join(dst_dir, new_file_name)
    os.rename(dst_file, new_dst_file_name)


def convert_object_entry(
    obj: dict, image_width: float, image_height: float, class_id_mapping: dict
):
    class_title = obj["classTitle"]

    class_id = class_id_mapping[class_title]

    class_counter[class_title] += 1

    left, top = obj["points"]["exterior"][0]
    right, bottom = obj["points"]["exterior"][1]

    mid_x = (left + right) / 2
    mid_y = (top + bottom) / 2

    bb_width = right - left
    bb_height = bottom - top

    norm_x = mid_x / image_width
    norm_y = mid_y / image_height

    norm_bb_width = bb_width / image_width
    norm_bb_height = bb_height / image_height

    if not (
        (0 <= norm_x <= 1)
        or (0 <= norm_y <= 1)
        or (0 <= norm_bb_width <= 1)
        or (0 <= norm_bb_height <= 1)
    ):
        raise RuntimeWarning(
            f"Normalized bounding box values outside the valid range! "
            f"x = {norm_x}; y = {norm_y}; w = {norm_bb_width}; h = {norm_bb_height}"
        )

    return class_id, norm_x, norm_y, norm_bb_width, norm_bb_height


def write_meta_data(
    darknet_export_base: Path, class_id_mapping: dict, num_labeled_images: int
):
    # write class id mapping

    with open(darknet_export_base / "classes.txt", "w") as class_info_file:

        for class_name, _ in sorted(class_id_mapping.items(), key=lambda kv: kv[1]):
            class_info_file.write("{}\n".format(class_name))

    # write stats

    print("Number of exported Images: {} ".format(num_labeled_images))
    print(class_counter)

    with open(darknet_export_base / "stats.txt", "w") as class_stat_file:

        class_stat_file.write("Number of images: {}\n\n".format(num_labeled_images))
        class_stat_file.write("Objects per class:\n")

        total_num_objects = 0

        for class_name, count in sorted(
            class_counter.items(), key=lambda kv: kv[1], reverse=True
        ):
            total_num_objects += count
            class_stat_file.write("{} -> {}\n".format(class_name, count))

        class_stat_file.write(
            "\nTotal number of objects: {}\n".format(total_num_objects)
        )


def main(sly_project_path: str, output_path: str):
    class_id_mapping = {
        name: darknet_id
        for darknet_id, name in enumerate(fsoco_classes(segmentation=False))
    }

    sly_base = Path(sly_project_path)
    darknet_export_base = Path(output_path)

    darknet_export_images_dir = darknet_export_base / "images"
    darknet_export_labels_dir = darknet_export_base / "labels"

    labels = list(sly_base.glob("*/ann/*.json"))

    clean_export_dir(darknet_export_images_dir, darknet_export_labels_dir)

    num_labeled_images = 0

    for label in labels:
        name = label.stem
        image = Path(str(label).replace("/ann/", "/img/").replace(".json", ""))

        with open(label) as json_file:
            data = json.load(json_file)

            if len(data["objects"]) > 0:
                num_labeled_images += 1

                image_width = data["size"]["width"]
                image_height = data["size"]["height"]

                export_image(darknet_export_images_dir, image, name)
                label_file_name = darknet_export_labels_dir / f"{name}.txt"

                with open(label_file_name, "w") as darknet_label:

                    for obj in data["objects"]:
                        try:
                            (
                                class_id,
                                norm_x,
                                norm_y,
                                norm_bb_width,
                                norm_bb_height,
                            ) = convert_object_entry(
                                obj,
                                image_height=image_height,
                                image_width=image_width,
                                class_id_mapping=class_id_mapping,
                            )

                            darknet_label.write(
                                "{} {} {} {} {}\n".format(
                                    class_id,
                                    norm_x,
                                    norm_y,
                                    norm_bb_width,
                                    norm_bb_height,
                                )
                            )
                        except RuntimeWarning as e:
                            click.echo(
                                f"[Warning] Failed to convert object entry in {label_file_name} \n -> {e}"
                            )

    write_meta_data(darknet_export_base, class_id_mapping, num_labeled_images)
