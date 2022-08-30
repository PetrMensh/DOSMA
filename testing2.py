import dosma
from dosma.core.med_volume import MedicalVolume
import numpy as np
import matplotlib.pyplot as plt
import math

path = "C:\\Users\\320071926\\Desktop\\knee_for_masking\\pat_2\\qDESS_low\\DICOM"


#-----------------------------------------------------------------------------------------------------------------------
# Read the data
#-----------------------------------------------------------------------------------------------------------------------
dr = dosma.DicomReader(verbose=True)
multi_echo_scan = dr.load(path, group_by=['EchoNumbers', 'AcquisitionNumber'])
a = tuple(multi_echo_scan)

S0 = a[int(len(a)/2)].volume[:, :, 34]
protocol_name = [a[int(len(a)/2)].get_metadata("ProtocolName")]
print(protocol_name)