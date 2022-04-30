import os
import copy
import sys

from processing_generated_data import processing_generated_data
from static_analysis_phase import static_analysis_phase

def run():
    
    static_analysis_phase()
    processing_generated_data()

run()
