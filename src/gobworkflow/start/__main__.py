"""Start relate jobs

Requires one or more catalogs to build relations to:

     python -m gobworkflow.start meetbouten
     python -m gobworkflow.start meetbouten nap
"""
import argparse
import sys

from gobcore.message_broker.config import EXPORT_QUEUE, IMPORT_QUEUE, REQUEST_QUEUE
from gobcore.message_broker import publish


class WorkflowCommands():

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog='python -m gobworkflow.start',
            description='Start GOB Jobs',
            epilog='Generieke Ontsluiting Basisregistraties',
            usage='''<command> [<args>]

The GOB workflow commands are:
   import       Start an import job for a collection
   export       Start an export job for a collection
   relate       Build relations for a catalog
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        command = f"{args.command}_command"
        if not hasattr(self, command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, command)()

    def import_command(self):
        parser = argparse.ArgumentParser(description='Start an import job for a collection')
        parser.add_argument('dataset_file',
                            nargs='+',
                            type=str,
                            help='a file containing the dataset definition')
        # Skip the first argument
        args = parser.parse_args(sys.argv[2:])
        for dataset_file in args.dataset_file:
            print(f"Trigger import of {dataset_file}")
            publish(IMPORT_QUEUE, "import.start", {"dataset_file": dataset_file})

    def export_command(self):
        parser = argparse.ArgumentParser(description='Start an export job for a collection')
        parser.add_argument('catalogue',
                            type=str,
                            help='the name of the data catalog (example: "meetbouten"')
        parser.add_argument('collection',
                            type=str,
                            help='the name of the data collection (example: "meetbouten"')
        parser.add_argument('filename',
                            type=str,
                            help='the name of the file to write the output to (example: "MBT_MEETBOUT.dat")')
        parser.add_argument('destination',
                            nargs='?',
                            type=str,
                            default="Objectstore",
                            choices=["Objectstore", "File"],
                            help='destination, default is Objectstore')
        # Skip the first argument
        args = parser.parse_args(sys.argv[2:])
        export_args = {
            "catalogue": args.catalogue,
            "collection": args.collection,
            "filename": args.filename,
            "destination": args.destination
        }
        print(f"Trigger export of {args.catalogue}.{args.collection} to {args.filename} on {args.destination}")
        publish(EXPORT_QUEUE, "export.start", export_args)

    def relate_command(self):
        parser = argparse.ArgumentParser(description='Build relations for a catalog')
        parser.add_argument('catalogue',
                            type=str,
                            help='the name of the data catalog (example: "meetbouten"')
        # Skip the first argument
        args = parser.parse_args(sys.argv[2:])
        print(f"Trigger build relations for {args.catalogue}")
        publish(REQUEST_QUEUE, "fullrelate.request", {"catalogue": args.catalogue})


def init():
    if __name__ == '__main__':
        WorkflowCommands()


init()