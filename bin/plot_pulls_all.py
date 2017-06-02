import os
import errno    
from ROOT import TFile, TH1D, TCanvas
import ROOT
from utils import read_category_ratios, readMisIDRatios, bin_names_composite, bin_names_composite_nice, read_exclude_bins
#, bin_names_single, mkdir_p, get_bin_name_single, get_bin_name, 
#from plot_pulls import 
from plot_pulls_gen import readMisIDRatiosGen, readCategoryRatiosGen, make_pull_plot_21
from matrix_solver import calculate_solution

NSIGMAS = 1.2815515 #Corresponds to p-value of 0.1
EXCLUDED_FILE = "../data/excluded_categories.txt"


def get_bin_nr_composite(cat):
  return bin_names_composite.index(cat)

def get_bin_nr_single(cat):
  return bin_names_single.index(cat)

def select_categories(chi2s):
  f = open(EXCLUDED_FILE, "w")
  for (k,v) in chi2s.items():
    #print k, v > NSIGMAS
    if v > NSIGMAS:
      f.write("%s\n" % k)
  f.close()

if __name__ == "__main__":
  ROOT.gROOT.SetBatch(True)
  infile = "/hdfs/local/ttH_2tau/andres/ttHAnalysis/2016/histosCF_summer_May30/histograms/charge_flip/histograms_harvested_stage2_charge_flip_Tight.root"  
  FITNAME = "summer_May30"
        
  misIDRatios = readMisIDRatiosGen(infile)
  catRatiosNum, catRatios = readCategoryRatiosGen(infile)
  chi2s = make_pull_plot_21(misIDRatios, catRatios, mydir = "pull_plots_all", y_range = (-0.002, 0.012))
  select_categories(chi2s)
  for exclude in [False, True]:
    fittypestring = "_gen"
    file_misId = "fit_output_pseudodata_%s/fit_res%s.root" % (FITNAME, fittypestring)
    name = "gen_fit"
    exclude_bins, exclude_bins_num = [], []
    if exclude:
      (exclude_bins, exclude_bins_num) = read_exclude_bins(EXCLUDED_FILE)
      name += "_exclusions"
      fittypestring += "_exclusions"
    file_misId = "fit_output_pseudodata_%s/fit_res%s.root" % (FITNAME, fittypestring)
    catRatiosNum, catRatios = readCategoryRatiosGen(infile, exclude_bins)
    #print catRatiosNum
    #print ":::"
    #print exclude_bins
    calculate_solution(catRatiosNum, exclude_bins_num, FITNAME, fittypestring, "pseudodata")
    print file_misId, fittypestring, exclude
    misIDRatios = readMisIDRatios(file_misId)
    make_pull_plot_21(misIDRatios, catRatios, mydir = "pull_plots_all", name = name, y_range = (-0.002, 0.012), excluded = exclude_bins)

  FITTYPE = "" #can use also "shapes" or "hybrid" here
  for datastring in ["pseudodata", "data"]:
    fittypestring = FITTYPE
    for exclude in [False, True]:
      if len(FITTYPE) > 0: fittypestring = "_"+FITTYPE
      file_cats = "fit_output_%s_%s/results_cat%s.txt" % (datastring, FITNAME, fittypestring)
      name = datastring
      exclude_bins, exclude_bins_num = [], []
      if exclude:
        (exclude_bins, exclude_bins_num) = read_exclude_bins(EXCLUDED_FILE)
        name += "_exclusions"
        fittypestring += "_exclusions"
      file_misId = "fit_output_%s_%s/fit_res%s.root" % (datastring, FITNAME, fittypestring)
      catRatiosNum, catRatios = read_category_ratios(file_cats, exclude_bins)
      calculate_solution(catRatiosNum, exclude_bins_num, FITNAME, fittypestring, datastring)
      misIDRatios = readMisIDRatios(file_misId)
      
      make_pull_plot_21(misIDRatios, catRatios, mydir = "pull_plots_all", name = name, y_range = (-0.002, 0.012), excluded = exclude_bins)
      #print misIDRatios
      #print "___________"
      #print catRatios
      #for exclude_categories in [True, False]:
      #  make_pull_plot_21(misIDRatios, catRatios, mydir = "pull_plots_all", name = datastring, exclude_categories = exclude_categories)
  
