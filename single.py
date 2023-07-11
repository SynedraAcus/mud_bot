#! python3.10

"""
A singleplayer engine for testing
"""
from argparse import ArgumentParser

from tgbot.clients.postgres_client import PSQLSceneStorage
from tgbot.engines.engines import SPEngine
from tgbot.world.test_scenes import TestStorage

if __name__ == "__main__":
    parser = ArgumentParser("Test singleplayer engine")
    parser.add_argument(
        "-s", type=str, default="local", help="Storage to use (local or postgres)"
    )
    args = parser.parse_args()
    if args.s == "local":
        storage = TestStorage()
    elif args.s == "postgres":
        storage = PSQLSceneStorage()
    else:
        raise ValueError(f"Invalid storage type {args.s}")
    e = SPEngine(storage, starting_scene="start")
    while True:
        e.process_input(input(">"))
