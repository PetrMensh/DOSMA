import dosma
from dosma.core.med_volume import MedicalVolume

dr = dosma.DicomReader(verbose=True)
multi_echo_scan = dr.load("F:\phantom_T2test_22.02.04\qdes_diffusion\medium_hard\DICOM", group_by=['EchoNumbers', 'ProtocolName'])
a = tuple(multi_echo_scan)
print(len(a))
print(a[0].get_metadata("ProtocolName"))
print(a[0].get_metadata("EchoTime"))
print(a[0].get_metadata("FlipAngle"))

print(a[1].get_metadata("ProtocolName"))
print(a[1].get_metadata("EchoTime"))
print(a[1].get_metadata("FlipAngle"))

print(a[2].get_metadata("ProtocolName"))
print(a[2].get_metadata("EchoTime"))
print(a[2].get_metadata("FlipAngle"))

print(a[3].get_metadata("ProtocolName"))
print(a[3].get_metadata("EchoTime"))
print(a[3].get_metadata("FlipAngle"))