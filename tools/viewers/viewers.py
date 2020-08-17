import click

from viewers.yolo.click_yolo_viewer import yolo


@click.group()
def viewers():
    """
    Label Viewers

    The commands in this group help you visualize your labels.
    If you're interested in extending the available viewers, have a look at:
    https://github.com/fsoco/fsoco/blob/master/tools/CONTRIBUTING.md
    """
    pass


viewers.add_command(yolo)


if __name__ == "__main__":
    print(
        "[LOG] This sub-module contains label viewers and is not meant to be run as a stand-alone script"
    )
