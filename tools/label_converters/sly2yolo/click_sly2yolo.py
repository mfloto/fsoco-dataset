import click

from .sly2yolo import main


@click.command()
@click.argument("sly_project_folder", type=str)
@click.argument("output_folder", type=str)
def sly2yolo(sly_project_folder, output_folder):
    """
     Supervisely  => Darknet YOLO format

    https://docs.supervise.ly/ann_format/

    \b
    The mapping between Darknet class IDs and the class names we use in FSOCO can be adapted in this file:
    tools/label_converters/class_id_to_fsoco.yaml

    \b
    Input:
    project_name
    ├── meta.json
    └── dataset_name
        ├── ann
        │   ├── img_x.json
        │   ├── img_y.json
        │   └── img_z.json
        └── img
            ├── img_x.jpeg
            ├── img_y.jpeg
            └── img_z.jpeg


    \b
    Output:

    output_folder
    ├──images_folder
       ├── img_x.jpeg
       ├── img_y.jpeg
       └── img_z.jpeg
    └── darknet_labels_folder
       ├── img_x.txt
       ├── img_y.txt
       └── img_z.txt


    """
    click.echo("[LOG] Running Supervisely to  Darknet Yolo label converter")
    main(sly_project_folder, output_folder)


if __name__ == "__main__":
    click.echo(
        "[LOG] This sub-module is not meant to be run as a stand-alone script. Please refer to\n $ fsoco --help"
    )
