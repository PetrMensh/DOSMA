import pydicom
from dosma.core.med_volume import MedicalVolume
import numpy as np
import matplotlib.pyplot as plt
import math

path = "F:\\New folder\\2\\DICOM\\IM_0033.dcm"

def dcm_clas_rd_philips(path):
    '''
    function allows to read image data and specific dicom tags
    Args:
        path: path to file

    Returns:
        image - image file (2D)
        ps_type - pulse sequence ('SPIN' or 'GRADIENT')
        te - echo time (ms)
        tr - repetition time (ms)
        fa -flip angle (degreases)
    '''
    ds = pydicom.dcmread(path)
    image = np.empty(shape=(ds.Rows, ds.Columns))
    image = ds.pixel_array
    te = ds[0x00180081].value  # echo time
    #ps_type = ds['EchoPulseSequence']
    ps_type = ds[0x2005140f][0][0x0018, 0x9008].value #pulse sequence name from privat tag
    #ps_type = ds[0x0018, 0x9008].value #pulse sequence name
    tr = ds[0x20051030].value #repetition time
    fa = ds[0x00181314].value #flip_angle
    print(ds)
    return image, ps_type, te, tr, fa

def weight_def(ps_type, te, tr, fa):
    '''

    Args:
        ps_type - pulse sequence ('SPIN' or 'GRADIENT')
        te - echo time (ms)
        tr - repetition time (ms)
        fa - flip angle (degreases)

    Returns:
        weight - weightning of the image ('T1', 'T2', 'PD')
    '''
    if ps_type == 'GRADIENT':
        if te < 15:
            if fa < 40:
                weight = 'PD'
            else:
                weight = 'T1'
        else:
            if fa < 40:
                weight = 'T2_star'
            else:
                weight = 'Not useful'

    elif ps_type == 'SPIN':
        if te < 15:
            if tr < 750:
                weight = 'T1'
            else:
                weight = 'PD'
        else:
            if tr < 750:
                weight = 'Not useful'
            else:
                weight = 'T2'
    return weight

(image, ps_type, te, tr, fa) = dcm_clas_rd_philips(path)
weight = weight_def(ps_type, te, tr, fa)
print(ps_type, te, tr, fa)
print(weight)




#(image, ps_type, te, tr, fa) = dcm_clas_rd_philips(path)






#-----------------------------------------------------------------------------------------------------------------------
# Read the data
#-----------------------------------------------------------------------------------------------------------------------
#dr = dosma.DicomReader(verbose=True)
#multi_echo_scan = dr.load(path, group_by=['EchoNumbers', 'AcquisitionNumber'])
#a = tuple(multi_echo_scan)

#S0 = a[int(len(a)/2)].volume[:, :, 34]
#protocol_name = [a[int(len(a)/2)].get_metadata("ProtocolName")]
#print(protocol_name)