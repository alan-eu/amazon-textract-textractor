from trp.trp2 import TDocument, TDocumentSchema, TextractBlockTypes
import trp.trp2 as t2
import trp.trp2_lending as tl
from textractprettyprinter.t_pretty_print import convert_form_to_list_trp2, convert_queries_to_list_trp2, \
    get_tables_string, convert_lending_from_trp2, convert_signatures_to_list_trp2, get_text_from_layout_json
from textractprettyprinter import get_layout_csv_from_trp2
import os
import json
import csv
import io


def test_pretty_with_tables():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(SCRIPT_DIR, "data", "w2-example.json")) as input_fp:
        textract_json = json.load(input_fp)
        tables_result = get_tables_string(textract_json=textract_json)
        assert tables_result
        tables_result = get_tables_string(textract_json=textract_json)
        assert len(tables_result) > 0

    with open(os.path.join(SCRIPT_DIR, "data", "employmentapp.json")) as input_fp:
        textract_json = json.load(input_fp)
        tables_result = get_tables_string(textract_json=textract_json)
        assert tables_result
        tables_result = get_tables_string(textract_json=textract_json)
        assert len(tables_result) > 0


def test_pretty_with_forms_and_trp2():

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/multi_page_example_file.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        trp2_doc = TDocumentSchema().load(json.load(input_fp))
        assert trp2_doc
        forms_as_list = convert_form_to_list_trp2(trp2_doc=trp2_doc)    #type: ignore
        assert len(forms_as_list) == 2
        assert len(forms_as_list[0]) == 30
        assert len(forms_as_list[1]) == 4


def test_pretty_with_queries_and_trp2():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/analyzeDocResponse.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        trp2_doc = TDocumentSchema().load(json.load(input_fp))
        assert trp2_doc
        queries_as_list = convert_queries_to_list_trp2(trp2_doc=trp2_doc)    #type: ignore
        assert len(queries_as_list) == 1
        assert len(queries_as_list[0]) == 3


def test_pretty_with_queries_and_trp2_one_without_answer():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/queries_one_no_answer.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        trp2_doc = TDocumentSchema().load(json.load(input_fp))
        assert trp2_doc
        queries_as_list = convert_queries_to_list_trp2(trp2_doc=trp2_doc)    #type: ignore
        assert len(queries_as_list) == 1
        assert len(queries_as_list[0]) == 9
        assert len([x for x in queries_as_list[0] if 'PAYSTUB_PERIOD_REGULAR_HOURLY_RATE' in x]) == 1
        assert len([x for x in queries_as_list[0] if 'PAYSTUB_PERIOD_START_DATE' in x]) == 1


def test_lending(caplog):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/lending-doc-output_from_output_config.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        trp2_doc: tl.TFullLendingDocument = tl.TFullLendingDocumentSchema().load(json.load(input_fp))    #type: ignore
        assert trp2_doc
        lending_array = convert_lending_from_trp2(trp2_doc)
        assert lending_array
        assert len(lending_array) > 900
        # import csv
        # with open("lending-output.csv", "w") as output_f:
        #     csv_writer = csv.writer(output_f)
        #     csv_writer.writerows(lending_array)


def test_pretty_with_signatures_and_trp2():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/request_for_verification_of_employment.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        trp2_doc = TDocumentSchema().load(json.load(input_fp))
        assert trp2_doc
        signatures_as_list = convert_signatures_to_list_trp2(trp2_doc=trp2_doc)    #type: ignore
        assert len(signatures_as_list) == 1
        assert len(signatures_as_list[0]) == 3


def test_queries_bouding_box_issue():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/bounding_box_issue.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        trp2_doc = TDocumentSchema().load(json.load(input_fp))
        assert trp2_doc
        queries_as_list = convert_queries_to_list_trp2(trp2_doc=trp2_doc)    #type: ignore
        form_as_list = convert_form_to_list_trp2(trp2_doc=trp2_doc)    #type: ignore
        signature_as_list = convert_signatures_to_list_trp2(trp2_doc=trp2_doc)    #type: ignore


def string_counter():
    # Dictionary to keep track of the occurrences of each string
    occurrences = {}

    def counter(string):
        # Increment the count for the given string
        if string in occurrences:
            occurrences[string] += 1
        else:
            occurrences[string] = 1

        # Return the current count of the string
        return occurrences[string]

    return counter


# Creating an instance of the counter


def test_layout_csv(caplog):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/layout_csv_example.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        trp2_doc: TDocument = TDocumentSchema().load(json.load(input_fp))    # type: ignore
        assert trp2_doc
        layout_csv = get_layout_csv_from_trp2(trp2_doc)
        csv_output = io.StringIO()
        csv_writer = csv.writer(csv_output, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for page in layout_csv:
            csv_writer.writerows(page)
        # print(csv_output)
        assert layout_csv[0][20][3] == "20"

def test_get_text_from_layout_json_multiple_headers_table():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    with (open(os.path.join(SCRIPT_DIR, "data", "multi_headers_table.json")) as input_fp,
          open(os.path.join(SCRIPT_DIR, "data", "multi_headers_table.txt")) as expected_fp):
        textract_json = json.load(input_fp)
        markdown = get_text_from_layout_json(textract_json=textract_json, generate_markdown=True)
        assert markdown and 1 in markdown
        assert markdown[1] == expected_fp.read()
