import dosma
from dosma.core.med_volume import MedicalVolume
import numpy as np
import matplotlib.pyplot as plt
import math

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

#-----------------------------------------------------------------------------------------------------------------------
# Inputs
#-----------------------------------------------------------------------------------------------------------------------
slice = 34
mask_names = ["mask_06", "mask_11", "mask_08", "mask_16", "mask_12", "mask_14"]
#mask_names = ["mask"]
mask_sizes = [[85, 175, 115, 205],
              [165, 115, 195, 145],
              [155, 235, 185, 265],
              [285, 65, 315, 95],
              [255, 165, 285, 195],
              [265, 265, 295, 295]]

path = "C:\Users\320071926\Desktop\knee_for_masking\pat_2\qDESS_low\DICOM"


#-----------------------------------------------------------------------------------------------------------------------
# Read the data
#-----------------------------------------------------------------------------------------------------------------------
dr = dosma.DicomReader(verbose=True)
multi_echo_scan = dr.load(path, group_by=['EchoNumbers', 'AcquisitionNumber'])
a = tuple(multi_echo_scan)

S0 = a[int(len(a)/2)].volume[:, :, slice]
protocol_name = [a[int(len(a)/2)].get_metadata("ProtocolName")]



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

#-----------------------------------------------------------------------------------------------------------------------
# Masks and
#-----------------------------------------------------------------------------------------------------------------------
values = []
mask_full = np.zeros((S.shape[1], S.shape[2]))
for j in range(0, len(mask_names)):
    mask = mask_creation(S.shape[1], S.shape[2], mask_sizes[j][0], mask_sizes[j][1], mask_sizes[j][2], mask_sizes[j][3])
    mask_full += mask
    values_mask = []
    for i in range(0, S.shape[0]):

        S0_masked = np.multiply(np.divide(S[i, :, :], S[0, :, :]), mask)
        S0_masked[S0_masked == 0] = np.nan
        percentil_temp = np.nanpercentile(S0_masked, [50])
        percentil_temp = float(percentil_temp[0])
        values_mask.append(percentil_temp)
    print(values_mask)
    values.append(values_mask)
    #print(values)

    plt.figure(dpi=200)
    imgplot = plt.imshow(np.multiply(S[0, :, :], mask_full), 'gray', interpolation='nearest')
    #imgplot = plt.imshow(S[0, :, :] - S[2, :, :], 'gray', interpolation='nearest')
    #imgplot.set_clim(-1, 1)
    plt.title('ADC map, 10^-3 mm^2/s')
    plt.colorbar()
    plt.savefig(path + '\\' + mask_names[j] + '.png')
    #plt.show()
    plt.close('all')

print(len(delta_k))
print(values[0])
delta_k[-2] = 105

plt.scatter(delta_k, values[0], c = 'red')
plt.scatter(delta_k, values[1], c = 'blue')
plt.scatter(delta_k, values[2], c = 'green')
plt.scatter(delta_k, values[3], c = 'orange')
plt.scatter(delta_k, values[4], c = 'grey')
plt.scatter(delta_k, values[5], c = 'black')
plt.xlabel('delta_k')
plt.ylabel('values')
plt.savefig(path + '\\' + mask_names[0] + '_graph.png')
#plt.show()
plt.close('all')


def theoretical_ADC_func(diffusivity, GlArea):
    alpha = 35
    TR = 13 * 1e-3
    T1 = 10000 * 1e-3
    Tg = 5000 * 1e-6

    Gl = GlArea / (Tg * 1e6) * 100
    gamma = 4258 * 2 * math.pi  # Gamma, Rad / (G * s).
    dkL = gamma * Gl * Tg
    print(dkL)
    alpha = math.radians(alpha)
    # Simply math
    k = (
            math.pow((math.sin(alpha / 2)), 2)
            * (1 + math.exp(-TR / T1 - TR * math.pow(dkL, 2) * diffusivity))
            / (1 - math.cos(alpha) * math.exp(-TR / T1 - TR * math.pow(dkL, 2) * diffusivity))
    )

    c1 = math.exp((-1) * (TR - Tg / 3) * (math.pow(dkL, 2)) * diffusivity)
    intensity = k * c1

    return intensity

diffusivity_list = np.arange(0.5e-9, 1.8e-9, 0.05e-9).tolist()
intensity_20 = list(map(lambda x: theoretical_ADC_func(x, 20), diffusivity_list))
intensity_110 = list(map(lambda x: theoretical_ADC_func(x, 110), diffusivity_list))
ratio = np.divide(intensity_110, intensity_20)
print(intensity_20)
print(intensity_110)
plt.scatter(diffusivity_list, ratio, c = 'red')
diffusivity_experimental = [0.665e-9, 1.155e-9, 0.854e-9, 1.651e-9, 1.201e-9, 1.484e-9]
ratio_experimental = [values[0][-1], values[1][-1], values[2][-1], values[3][-1], values[4][-1], values[5][-1]]
plt.scatter(diffusivity_experimental, ratio_experimental, c = 'blue')
plt.show()