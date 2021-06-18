"""
    amalthea - the world's history in the ethereum network

    GNU GENERAL PUBLIC LICENSE
"""
import sys

sys.path.insert(1, '../')
from hermes.get_pages_revisions import get_page_revisions

def main():  
    page = "Alfaview"
    get_page_revisions(page)


if __name__ == "__main__":
    main()
