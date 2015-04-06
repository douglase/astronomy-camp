# Introduction #

This procedure needs to be run on the observer computer in the ARO 12m (remotely is fine). Change target names as appropriate.
See also: http://aro.as.arizona.edu/docs/analysis_manuals.htm
The scripts referred to below, and called with `@P:` are located on modelo in: **/home/obs/GAG/**

# **Details** #

In terminal:
```
otf2class -bs # -es # -i (1 or 2) -s 10 -d -o /home/obs/ _directory_ _filename_
```
where `bs` and `es` are the beginning and end scan numbers.

Open `class` from command line and
initialize with `@P:startx`
The print from this command should include the following glossary of shortcuts:
```
symbol mx "las\set mode x"
LAS_3> symbol my "las\set mode y"
LAS_3> symbol ss "las\SET Source"
LAS_3> symbol sl "las\set line"
LAS_3> symbol ssc "las\set scan"
LAS_3> symbol so "las\set off"
LAS_3> symbol b1 "las\base 1"
LAS_3> symbol sw "las\set window"
LAS_3> symbol fi "las\file in"
LAS_3> symbol fo "las\file out"
LAS_3> symbol st "las\set telescope"
```


to select backend use "set telescope" or "st", i.e. `st 12m-Mac`.
```
file in class_010.12m

ss "nameofsource"
set number 533 624
```
for example, files look like:
_class\_006.12m through class\_009.12m_
% so need to run sequence on each and then combine.

%1st for each file convert the on the fly file to a class file. specify 1st record and last, use backend 3 and 4 and debug and put in the aac folder:
```
otf2class -bs 1953 -es 1960 -i 3 -d -o /home/obs/aac/ sdd.aac_006
otf2class -bs 1962 -es 2043 -i 3 -d -o /home/obs/aac/ sdd.aac_007
otf2class -bs 2045 -es 2126 -i 3 -d -o /home/obs/aac/ sdd.aac_008
otf2class -bs 2131 -es 2212 -i 3 -d -o /home/obs/aac/ sdd.aac_009
```
%skipped @scaleall and @P:baseallkill since they seemed superfluous.

%In class:
```
fi class.sdd_fb21.aac_006
find
list
```
%define a window, use fact that  VLSR is x km/s:

To preview the first profile and determine the window, get a record, view the header and plot:
```
get 1
header
plot
```

%could use base all kill but don't need to, channels look ok and can window out.

```
@P:baseall
% (if no bad channel)
J=1
%created:
w3irs5_006.base.base
w3irs5_007.base.base
w3irs5_008.base.base
```

complete data range:
```
mx -400 300
```

window including line window:
```
sw -100 0.
```


A quick sequence might look like:
```
ss “nameofsource”
find
list
sw (block out line and bad channels)
mx -10 28
@P:baseallkill (if bad channel)
Bad channel # (50)
sourcename_fb11.base
file in sourcename_fb11.base
find
list
@P:scaleall
calibration factor # (on the order of 1.05)
sourcename_fb11.scale

file in class.sdd_fb12.khu_001
find
list
@P:baseall (if no bad channel)
J=1
sourcename_fb12.base
file in sourcename_fb12.base
find
list
@P:scaleall
calibration factor # (on the order of 0.95)
sourcename_fb12.scale
file in sourcename_fb12.scale
find
list
@P:combine
sourcename_fb11.scale
correct scan #
file in sourcename_fb11.scale
find
list
@P:convall
```
The `convall` script will ask for the following parameters:
```
lmin -210 #MIN RA offset (in units of ARCSEC) 
lmax 210 #MAX RA offset (in units of ARCSEC) 
bmin -300 #MIN Dec offset (in units of ARCSEC) 
bmax 300 ##MAX Dec offset (in units of ARCSEC) 
step size 30
new beam 20
old beam 2
sourcename.conv
```
```
file in sourcename.conv
find
list
my -2 3
@P:mapcso
hardcopy filename.ps /device ps color
```

**_Contour Mapping_**
```
class
@P:startx
file in cluster*.conv
mx -2 18
find
list
print area -2 18 /output cluster*.area
exit
greg
@P:con
cluster*.area
2
3
4
n
(0.06 to 0.13522 by 0.025)
n
n
“Title”
“Object”
hardcopy cluster*.ps /device ps color
```