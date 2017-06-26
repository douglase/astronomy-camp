# Now load IRAF
import pyraf.iraf as iraf
import os
from os.path import expanduser


os.system("mkiraf")


# Load the packages we might need.

iraf.noao(_doprint=0)
iraf.onedspec(_doprint=0)
iraf.twodspec(_doprint=0)
iraf.apextract(_doprint=0)
iraf.unlearn(iraf.apall)
iraf.unlearn(iraf.identify)
text_file = open("filename.txt", "r")
filename=text_file.readline()
text_file.close()
home = expanduser("~/")
import pickle

# load file names:
with open('filenames.pickle') as f:  # Python 3: open(..., 'rb')
    dataset, target, filename,extracted_filename,  calibrated_filename, crval, dispersion = pickle.load(f)


# Delete some directories/files from previous runs:
os.system("rm -rf login.cl database pyraf uparm")
os.system("rm "+ calibrated_filename)

iraf.identify(filename[:-5], coordli=home+"/Downloads/HgNe(1).dat",
              section="line 105 125",
              crval=crval,
              cdelt=dispersion,
              fwidth=5)

# Tell the extracted spectrum what the wavelength solutions are.
iraf.hedit(images=[extracted_filename],
           fields=["REFSPEC1"], \
        value=[filename], add="Yes")
iraf.refspec(input = extracted_filename,referen=filename[:-5],sort='',group='',confirm='no')
iraf.dispcor(input=extracted_filename,
             output=calibrated_filename)

# Plot the extracted spectrum?
iraf.splot(calibrated_filename)
