import dosma
from dosma.core.med_volume import MedicalVolume
import numpy as np
import matplotlib.pyplot as plt

def mask_creation(x_dim, y_dim, x_0, y_0, x_1, y_1):
    mask = np.zeros((x_dim, y_dim))
    mask[x_0:x_1, y_0:y_1] = 1
    return mask

def numb_extraction(string):
    num = ''
    for character in string:
        if character.isdigit() == True:
            num += str(character)
    return int(num)


slice = 60
mask_names = ["mask_06", "mask_11", "mask_08", "mask_16", "mask_12", "mask_14"]
#mask_sixes = [[],
#              [],
#              [],
#             [],
#              [],
#              []]

path = "E:\CRIEPST\phantom_qDESS_different_GRAD\DICOM"

dr = dosma.DicomReader(verbose=True)
multi_echo_scan = dr.load(path, group_by=['EchoNumbers', 'ProtocolName'])
a = tuple(multi_echo_scan)


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
protocol_name.remove(protocol_name[0])
delta_k = list(map(lambda x: numb_extraction(x), protocol_name))
print(delta_k)

mask = mask_creation(S.shape[1], S.shape[2], 130, 130, 150, 150)

values = []
for i in range(0, S.shape[0]):
    S0_masked = np.multiply(S[i, :, :], mask)
    S0_masked[S0_masked == 0] = np.nan
    percentil_temp = np.nanpercentile(S0_masked, [50])
    percentil_temp = float(percentil_temp[0])
    values.append(percentil_temp)
print(values)

plt.figure(dpi=200)
#imgplot = plt.imshow(np.multiply(S[0, :, :] - S[4, :, :], mask), 'gray', interpolation='nearest')
imgplot = plt.imshow(S[0, :, :] - S[1, :, :], 'gray', interpolation='nearest')
imgplot.set_clim(-1, 1)
plt.title('ADC map, 10^-3 mm^2/s')
plt.colorbar()
plt.savefig(path + '\\' + mask_names[0] + '.png')
plt.show()

plt.scatter(delta_k, values)
plt.xlabel('delta_k')
plt.ylabel('values')
plt.savefig(path + '\\' + mask_names[0] + '_graph.png')
plt.show()
plt.close('all')