# This is Panoramix, PostTexRST to FinalRST converter for PyColore. This simply
# does some processing after pandoc converts Tex files to RST.

import click

@click.group()
def panoramix():
    """Programme Panoramix. Il sait faire plein de choses, surtout des potions."""
    pass

from .makedocs import makedocs

if __name__ == '__main__':
    panoramix()