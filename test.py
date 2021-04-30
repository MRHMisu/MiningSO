import sys
import re
from xml.etree import ElementTree as ET


def extract_tags(posts_xml_path):
    xml_parser = ET.iterparse(posts_xml_path)
    for rc, (event, element) in enumerate(xml_parser):
        if element.tag == "row":
            if element.get("PostTypeId") == "1":  # explore the question
                tages = str(element.get("Tags"))
                pattern_open_tag = r'<'
                removed_open_tag = re.sub(pattern_open_tag, '', tages)
                pattern_close_tag = r'>'
                removed_close_tag = re.sub(pattern_close_tag, ',', removed_open_tag)
                tags_csv = removed_close_tag.rstrip(removed_close_tag[-1])
                print(tags_csv)
        element.clear()


if __name__ == "__main__":
    so_post_xml_path = "sample-so-posts.xml"
    extract_tags(so_post_xml_path)
    sys.exit()
