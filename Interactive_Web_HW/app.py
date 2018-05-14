from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd
import datetime as dt
import numpy as np


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

engine=create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

session=Session(bind=engine)

Base = automap_base()

Base.prepare(engine, reflect=True)

Samples = Base.classes.samples
Metadata = Base.classes.samples_metadata
OTU = Base.classes.otu


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

@app.route("/names")
    # List of sample names.
    # Returns a list of sample names in the format
    # [
    #     "BB_940",
    #     "BB_941",
    #     "BB_943",
    #     "BB_944",
    #     "BB_945",
    #     "BB_946",
    #     "BB_947",
    #     ...
    # ]

def names():    
    results = session.query(samples)
    list_names = list(session.execute(results).keys())
    full_name_list = list_names[1:]
    return jsonify(full_name_list)


@app.route("/otu")
    # """  Returns a list of OTU descriptions in the following format
    # [
    #     "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
    #     "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
    #     "Bacteria",
    #     "Bacteria",
    #     "Bacteria",
    #     ...
    # ]
    # """
def otu_list():    
    results = session.query(OTU.lowest_taxonomic_unit_found).all()
    descriptions = results
    return jsonify(descriptions)


@app.route("/metadata/<sample>")

    # """Returns metadata for a given sample
    # Args: Sample in the format:'BB_940'
    # returns a json dict of metadata like so:
    # {
    #     Age: 24,
    #     BBTYPE: "I",
    #     ETHNICITY: "Caucasian",
    #     GENDER: "F",
    #     LOCATION: "Beaufort/NC",
    #     SAMPLEID: 940
    # }
    # """
def metadata(sample):
    results = session.query(Metadata.AGE, Metadata.BBTYPE, Metadata.ETHNICITY, Metadata.GENDER, Metadata.LOCATION, Metadata.SAMPLEID).filter(Metadata.SAMPLEID == "BB_" + sample)
    metadata_list = []
    for result in results:
        row = {}
        row["Age"] = result[0]
        row["BBType"] = result[1]
        row["Ethnicity"] = result[2]
        row["Gender"] = result[3]
        row["Location"] = result[4]
        row["SampleID"] = result[5]
        metadata_list.append(row)
    return jsonify(metadata_list)

# Returns an integer value for the weekly washing frequency `WFREQ`
@app.route('/wfreq/<sample>')
def sample_wfreq(sample):
    """Return the Weekly Washing Frequency as a number."""
    sampleID=int(sample.split("_")[1])
    results = session.query(Metadata.WFREQ).\
        filter(Metadata.SAMPLEID == sampleID).first()
    wfreq = int(results)
    # Return only the first integer value for washing frequency
    return jsonify(wfreq)


@app.route('/samples/<sample>')

    # """OTU ID's and Sample Values for a given sample.
    # sort by Sample Value in descending order, return a list of dictionaries for
    # 'otu_ids' and 'sample_values'
    # [
    #     {
    #         otu_ids: [
    #             1166,
    #             2858,
    #         ],
    #         sample_values: [
    #             163,
    #             126,
    #         ]
    #     }
    # ]
    # """
def otu_id_values(sample):
    results = session.execute("SELECT otu_id, "+sample+" FROM samples ORDER BY "+sample+" DESC").fetchall
    # Create lists of otu_ids and values
    otus = [item[0] for item in results]
    values = [item[1] for item in results]  

    # Place the lists into an object
    otus_and_values = {"otu_ids": otus, "sample_values": values}
    return jsonify(otus_and_values)
    
if __name__ == '__main__':
    app.run(debug=True)
