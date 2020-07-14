import click
from similarity_scorer.utils.logger import Logger
from collect_stats.stats_collector import StatsCollector


@click.command()
@click.argument("sly_project_name", type=str)
@click.option(
    "--calc_similarity", is_flag=True, help="Calculate the image similarity stats."
)
@click.option(
    "--num_workers",
    default=4,
    help="Number of workers for feature extraction process, max number depends on GPU memory!",
    type=click.IntRange(1, 256),
)
@click.option("--gpu", is_flag=True, help="Use GPU for feature extraction")
def collect_stats(
    sly_project_name: str, calc_similarity: bool, num_workers: int, gpu: bool
):
    """
    Collect stats from a local supervisely project for later analysis.

    \b
    Usage:
    fsoco collect_stats SLY_PROJECT_NAME

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


    """

    Logger.log_info("Start collecting stats")

    collector = StatsCollector(calc_similarity, num_workers, gpu)
    if collector.load_sly_project(sly_project_name):
        image_df, box_df = collector.collect_stats()

        image_df_filename = f"{sly_project_name}_image_stats.df"
        bbox_df_filename = f"{sly_project_name}_bbox_stats.df"

        image_df.to_pickle(image_df_filename)
        box_df.to_pickle(bbox_df_filename)

        Logger.log_info(f"Saved per image stats to '{image_df_filename}'")
        Logger.log_info(f"Saved per image stats to '{bbox_df_filename}'")


if __name__ == "__main__":
    click.echo(
        "[LOG] This sub-module is not meant to be run as a stand-alone script. Please refer to\n $ fsoco --help"
    )
