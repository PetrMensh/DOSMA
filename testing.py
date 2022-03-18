import dosma
from dosma.core.med_volume import MedicalVolume
import numpy as np
import matplotlib.pyplot as plt

def mask_creation(x_dim, y_dim, x_0, y_0, x_1, y_1):
    mask = np.zeros((x_dim, y_dim))
    mask[x_0:x_1, y_0:y_1] = 1
    return mask

dr = dosma.DicomReader(verbose=True)
multi_echo_scan = dr.load("E:\CRIEPST\phantom_qDESS_different_GRAD\DICOM", group_by=['EchoNumbers', 'ProtocolName'])
a = tuple(multi_echo_scan)


slice = 70
S0 = a[int(len(a)/2)].volume[:, :, slice]
protocol_name = [a[int(len(a)/2)].get_metadata("ProtocolName")]
print(a[int(len(a)/2)].get_metadata("ProtocolName"))
print(a[int(len(a)/2)].get_metadata("EchoTime"))
print(a[int(len(a)/2)].get_metadata("FlipAngle"))

S = np.empty(shape=(S0.shape[0], S0.shape[1]))
S = np.expand_dims(S, axis=0)

for i in range(int(len(a)/2), len(a)):
    print(a[i].get_metadata("ProtocolName"))
    print(a[i].get_metadata("EchoTime"))
    print(a[i].get_metadata("FlipAngle"))
    S_temp = np.expand_dims(a[i].volume[:, :, slice], axis=0)
    protocol_name_temp = a[i].get_metadata("ProtocolName")
    S = np.vstack((S, S_temp))
    protocol_name.append(protocol_name_temp)
S = np.delete(S, (0), axis=0)

#S0 = a[8].volume[:, :, 70]
#S1 = a[9].volume[:, :, 70]
#S2 = a[10].volume[:, :, 70]
#S3 = a[11].volume[:, :, 70]
#S4 = a[12].volume[:, :, 70]
#S5 = a[13].volume[:, :, 70]
#S6 = a[14].volume[:, :, 70]
#S7 = a[15].volume[:, :, 70]

print(S.shape[1])
mask = mask_creation(S.shape[1], S.shape[2], 130, 130, 150, 150)
print(mask.max())

for i in range(0, S.shape[0]):
    S0_masked = np.multiply(S[i, :, :], mask)
    S0_masked[S0_masked == 0] = np.nan
    percentil = np.nanpercentile(S0_masked, [25, 50, 75])
    print(percentil)

#clim_values = np.nanpercentile(S[0, :, :], [5, 50, 95])
plt.figure(dpi=200)
imgplot = plt.imshow(np.multiply(S[0, :, :], mask), 'gray', interpolation='nearest')
#imgplot = plt.imshow(np.multiply(S[0, :, :], mask), 'jet', interpolation='nearest')
#imgplot.set_clim(clim_values[0], clim_values[2])
plt.title('ADC map, 10^-3 mm^2/s')
plt.colorbar()
plt.show()
#plt.savefig(folder + '\\' + str(dcm_general_dict['Patient_name']) + '_' + mask_name + '_ADC_map_slice' + str(mask.shape[0] - i) + '.png')
plt.close('all')

#b = a[8].volume
#print(type(b[:, :, 70]))