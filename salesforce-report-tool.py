import os
import base64
import yaml
import json
from salesforce_reporting import Connection
import datetime
import tkinter as tk


def main():
    """
    Main function
    """

    sf = create_salesforce_client()

    root= tk.Tk()

    canvas1 = tk.Canvas(root, width = 500, height = 300,  relief = 'raised')
    canvas1.pack(side=tk.TOP, fill=tk.Y)

    label1 = tk.Label(root, text='Cloudreach Payment Automation')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)

    label2 = tk.Label(root, text='Input Report ID:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 100, window=label2)

    entry1 = tk.Entry (root)
    canvas1.create_window(200, 140, window=entry1)

    def run_report():
        report_id = entry1.get()

        label3 = tk.Label(root, text= 'Report Contains:',font=('helvetica', 10))
        canvas1.create_window(200, 210, window=label3)

        report_original = sf.get_report(report_id, details=True)
        column_names = get_column_names(report_original)
        fact_map_key = get_fact_map_key(report_original)
        report_json = refine_report(report_original, fact_map_key, column_names)

        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(root, yscrollcommand=scrollbar.set, height=30, width=100)
        report_use = json.loads(report_json)
        for key, value in report_use["report_data"].items():
            for key, value in value.items():
                listbox.insert(tk.END, key + ": " + value)
            listbox.insert(tk.END, "-----")
        listbox.pack(side=tk.BOTTOM, fill=tk.BOTH)

        scrollbar.config(command=listbox.yview)

    button1 = tk.Button(text='Run Report', command=run_report, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 180, window=button1)

    root.mainloop()


def create_salesforce_client():
    """
    Create Salesforce Client using credential files
    """

    dirname = os.path.dirname(__file__)
    sf_creds = os.path.join(dirname, 'salesforce-creds.yaml')

    sf_creds_file = os.path.expanduser(sf_creds)
    with open(sf_creds_file) as f:
        sf_creds = yaml.safe_load(f)

    print(sf_creds)

    sf = Connection(
        username=sf_creds["username"],
        password=base64.b64decode(sf_creds["password"]).decode(),
        security_token=sf_creds["access_token"]
    )

    return sf


def get_column_names(report_original):
    """
    Get list of column names, order is consistent for each row
    """

    column_names = []

    for key, value in report_original["reportExtendedMetadata"]["detailColumnInfo"].items():
        column_names.append(value.get("label"))

    return column_names


def get_fact_map_key(report_original):
    """
    Get fact map key
    """

    for key, value in report_original["factMap"].items():
        fact_map_key = key

    return fact_map_key


def refine_report(report_original, fact_map_key, column_names):
    """
    Extract required fields from original report and create new JSON object
    """

    report_name = report_original["attributes"]["reportName"]
    report_id = report_original["attributes"]["reportId"]
    report_datetime = str(datetime.datetime.now().time())
    report_currency = report_original["reportMetadata"]["currency"]
    for aggregates in report_original["factMap"][fact_map_key]["aggregates"]:
        report_rows_total = aggregates.get("label")

    report_dict = {
        "report_name": report_name,
        "report_id": report_id,
        "report_datetime": report_datetime,
        "report_currency": report_currency,
        "report_rows_total": report_rows_total,
        "report_data": {}
    }

    for i_row, row in enumerate((report_original["factMap"][fact_map_key]["rows"]), 1):
        row_name = ("row_" + str(i_row))
        report_dict["report_data"][row_name] = {}
        for i_data_cells, data_cells in enumerate(row["dataCells"]):
            report_dict["report_data"][row_name][column_names[i_data_cells]] = data_cells.get("label")

    report_json = json.dumps(report_dict)

    return report_json


if __name__ == '__main__':
    main()
