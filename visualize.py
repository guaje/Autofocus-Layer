#import matplotlib
#matplotlib.use('GTK3Cairo')
import matplotlib.pyplot as plt
import os
import SimpleITK as sitk

fname = os.path.join('/home/jrguajeg/Devel/workshop/dl/Autofocus-Layer/result/AFN1',
                     'VSD.brats_tcia_pat111_0001.42287.mha')

mr_image = sitk.ReadImage(fname)
npa = sitk.GetArrayViewFromImage(mr_image)

# Display the image slice from the middle of the stack, z axis
z = int(mr_image.GetDepth()/2)
npa_zslice = sitk.GetArrayViewFromImage(mr_image)[z, :, :]

# Three plots displaying the same data, how do we deal with the high dynamic range?
fig = plt.figure()
fig.set_size_inches(15, 30)

fig.add_subplot(1, 3, 1)
plt.imshow(npa_zslice)
plt.title('default colormap')
plt.axis('off')

fig.add_subplot(1, 3, 2)
plt.imshow(npa_zslice, cmap=plt.cm.Greys_r)
plt.title('grey colormap')
plt.axis('off')

fig.add_subplot(1, 3, 3)
plt.title('grey colormap,\n scaling based on volumetric min and max values')
plt.imshow(npa_zslice, cmap=plt.cm.Greys_r, vmin=npa.min(), vmax=npa.max())
plt.axis('off')

plt.show()
