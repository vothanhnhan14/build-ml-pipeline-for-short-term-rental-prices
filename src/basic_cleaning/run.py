#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info(f'Downloading artifact {args.input_artifact} ...')
    csv_file_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(csv_file_path)

    logger.info(f'Drop outlier price values')
    df = df[df['price'].between(args.min_price, args.max_price)]

    logger.info('Convert last_review to datetime')
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info(f'Upload artifact {args.output_artifact}')
    df.to_csv('clean_sample.csv', index=False)
    out_artifact = wandb.Artifact(args.output_artifact, 
                                  type=args.output_type, 
                                  description=args.output_description)
    out_artifact.add_file('clean_sample.csv')
    run.log_artifact(out_artifact)

    run.finish()
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Very basic cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="The output type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="The output description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="The minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="The maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
