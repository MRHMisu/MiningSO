"""
Extract rows from snippets from the SO dump (Posts.xml) file filtered by year timestamp.
"""

# Example snippets of Posts.xml
# <row Id="4" PostTypeId="1" AcceptedAnswerId="7" Tags="&lt;discussion&gt;" AnswerCount="2" CommentCount="0" />
# <row Id="7" PostTypeId="2" ParentId="4" />
# PostTypeId="1" represents Question and PostTypeId="2" represents Answer


import sys
from datetime import datetime
from xml.etree import ElementTree as ET


def extract_code_snippets(posts_xml_path, output_path, batch, from_timestamp, to_timestamp):
    """
    extract stackoverflow data dump to with a given time frame
    :param posts_xml_path: SO Post.xml file path
    :param output_path: output file path
    :param batch: number of lines to write into the output file at once
    :param from_timestamp: from_timestamp for instance, "2020-03-01T00:00:00.000"
    :param to_timestamp: to_timestamp for instance, "2021-03-01T00:00:00.000"
    :return: write the extracted post in output file in batch mode
    """
    xml_parser = ET.iterparse(posts_xml_path)
    from_timestamp = datetime.fromisoformat(from_timestamp)
    to_timestamp = datetime.fromisoformat(to_timestamp)
    post_count = 0
    year_range_post_list = []

    for rc, (event, element) in enumerate(xml_parser):
        print("Process " + str(rc) + " rows")
        if element.tag == "row":
            post_creation_date = datetime.fromisoformat(element.get("CreationDate"))
            if from_timestamp <= post_creation_date <= to_timestamp:
                post_count += 1
                post = ET.tostring(element, encoding='unicode')
                year_range_post_list.append(post)
                post_len = len(year_range_post_list)
                if post_len == batch:
                    print("Collected Post length  " + str(post_len))
                    print("Collecting " + str(post_count) + " snippets")
                    write_lines(year_range_post_list, output_path)
                    year_range_post_list.clear()
    write_lines(year_range_post_list, output_path)
    print("Collecting " + str(post_count) + " snippets")


def write_lines(contents, path):
    file_writer = open(path, 'a')
    file_writer.writelines(contents)
    file_writer.close()


def write_line(content, path):
    file_writer = open(path, 'a')
    file_writer.write(content)
    file_writer.close()


if __name__ == "__main__":
    # The data dump for SO Post.xml was created at 01-Mar-2021 17:33

    # # run this script with 5 arguments
    so_post_xml_path = sys.argv[1]  # SO Post.xml file path
    year_post_output_path = sys.argv[2]  # output file path .xml
    batch_size = int(sys.argv[3])  # number of lines to write into the output file at once
    from_date = sys.argv[4]  # from_timestamp for instance, "2020-03-01T00:00:00.000"
    to_date = sys.argv[5]  # t0_timestamp for instance, "2021-03-01T00:00:00.000"

    # Testing purpose
    # so_post_xml_path ="sample-so-posts.xml"
    # year_post_output_path ="tt.xml"
    # batch_size =2
    # from_date = "2008-07-01T00:00:00.000"
    # to_date = "2008-08-03T00:00:00.000"

    # run on cmd with 5 arguments
    # python3 Post.xml year_output.xml 5000 "2020-03-01T00:00:00.000" "2021-03-01T00:00:00.000"

    XML_DEFINITION = "<?xml version='1.0' encoding='utf-8'?>"
    OPENING_TAG = "<posts>"
    CLOSING_TAG = "</posts>"

    firstLine = XML_DEFINITION + '\n' + OPENING_TAG + '\n'
    write_line(firstLine, year_post_output_path);

    extract_code_snippets(so_post_xml_path, year_post_output_path, batch_size, from_date, to_date)

    write_line(CLOSING_TAG, year_post_output_path)
    sys.exit()
