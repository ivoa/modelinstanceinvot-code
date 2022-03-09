#!/usr/bin/env python
import http
from astropy.io.votable import parse

# Uncomment for user entries
# filterBand = input("Please enter Filter/Band e.g. 2MASS/2MASS.H: ")
templateFile = 'photdm_filter_template.xml'
referenceSpectrum = "http://svo2.cab.inta-csic.es/theory/fps/morefiles/vega.dat"

#filterBand = "2MASS/2MASS.Ks"
filterBands = ["GAIA/GAIA2.G", 
               "2MASS/2MASS.J", "2MASS/2MASS.H", "2MASS/2MASS.Ks", 
               "WISE/WISE.W1", "WISE/WISE.W2", "WISE/WISE.W3", "WISE/WISE.W4"]

for filterBand in filterBands:
    print("=== Processing " + filterBand)
    outputFile = "./photdm." + filterBand.replace("/", ".") + ".xml"
    vegaFile = "./vega." + filterBand.replace("/", ".") + ".xml"
    photSystem = filterBand.split('/')[0]
    fpsServer = "svo2.cab.inta-csic.es"
    fpsQuery = "/theory/fps/fps.php?PhotCalID=" + filterBand + "/Vega"
    fpsServiceURL = "http://svo2.cab.inta-csic.es/theory/fps/fps.php?PhotCalID="
    fpsVOTable = fpsServiceURL + filterBand + "/Vega"
    
    referenceMagnitudeValue = 0
    
    with open(vegaFile, "w") as output:
        print("download " + vegaFile)
        conn = http.client.HTTPConnection(fpsServer) 
        conn.request('GET', fpsQuery)
        r1 = conn.getresponse()
        page = r1.read().decode('utf-8')
        output.write(page)
    
    votable = parse(vegaFile)
    table = votable.get_first_table()
    
    #Setting defaults (add here values that are not always present)
    bandName = ""
    sys_dmid = "_sys_" + filterBand.split("/")[1].replace(".", "_")
    cal_dmid = "_cal_" + filterBand.split("/")[1].replace(".", "_")
    filter_dmid = "_filter_" + filterBand.split("/")[1].replace(".", "_")
    # We need to iterate on the params (looks a limitation of the library) and we fill-in 
    # variables for the replacement. This could be probably simplified with a set but, at least
    # it is quite easy to identify possible problems in this approach
    for param in table.params: # retrieving table.params
        if param.utype  == "photdm:PhotometricSystem.detectorType":
            detectorType = param.value
        if param.utype  == "photdm:PhotCal.identifier":
            photCalIdentifier = param.value
        if param.utype  == "photdm:PhotCal.MagnitudeSystem.type":
            magnitudeSystemType = param.value
        if param.utype  == "photdm:PhotCal.ZeroPoint.type":
            zeroPointType = param.value
        if param.utype  == "photdm:PhotCal.ZeroPoint.Flux.value":
            zeroPointFluxValue = param.value
            zeroPointFluxUnit = param.unit;
        if param.utype  == "PhotometryFilter.fpsIdentifier":
            photometryFilterFpsIdentifier = param.value
        if param.utype  == "photdm:PhotometryFilter.identifier":
            photometryFilterIdentifier = param.value
        if param.utype  == "photdm:PhotometryFilter.description":
            photometryFilterName = param.value
            photometryFilterDescription = param.value
        if param.utype  == "photdm:PhotometryFilter.identifier":
            photometryFilterIdentifier = param.value
        if param.utype  == "photdm:PhotometryFilter.bandName":
            bandName = param.value
        if param.name  == "WavelengthEff":
            spectralLocation = param.value
            spectralLocationUCD = param.ucd
        if param.utype  == "photdm:PhotometryFilter.SpectralAxis.Coverage.Bounds.Extent":
            bandwidthExtent = param.value
        if param.utype  == "photdm:PhotometryFilter.SpectralAxis.Coverage.Bounds.Start":
            bandwidthStart = param.value
        if param.utype  == "photdm:PhotometryFilter.SpectralAxis.Coverage.Bounds.Stop":
            bandwidthStop = param.value
    
    
    with open(templateFile, 'r') as template:
        print("Read template " + templateFile)
        data = template.read()
    
    #Substitution of variables
    from string import Template
    the_template = Template(data)
    result = the_template.substitute(
        sys_dmid = sys_dmid,
        cal_dmid = cal_dmid,
        filter_dmid = filter_dmid,
        photSystem = photSystem,
        detectorType = detectorType,
        photCalIdentifier = photCalIdentifier,
        magnitudeSystemType = magnitudeSystemType,
        referenceSpectrum = referenceSpectrum,
        zeroPointType = zeroPointType,
        referenceMagnitudeValue = referenceMagnitudeValue,
        zeroPointFluxUnit = zeroPointFluxUnit,
        zeroPointFluxValue = zeroPointFluxValue,
        photometryFilterFpsIdentifier = photometryFilterFpsIdentifier,
        photometryFilterIdentifier = photometryFilterIdentifier,
        photometryFilterName = photometryFilterName,
        photometryFilterDescription = photometryFilterDescription,
        bandName = bandName,
        spectralLocation = spectralLocation,
        spectralLocationUCD = spectralLocationUCD,
        bandwidthExtent = bandwidthExtent,
        bandwidthStart = bandwidthStart,
        bandwidthStop = bandwidthStop,
        fpsVOTable = fpsVOTable)
    
    #write result
    print("Write output in " + outputFile)
    with open(outputFile, "w") as phot_file:
        phot_file.write(result)
    
