from fury import actor, ui, window

import nibabel as nib
import numpy as np
import os
import SimpleITK as sitk


sdir = os.path.abspath(os.path.dirname('__file__'))
resdir = 'result/AFN6'
imgdir = 'HGG/brats_tcia_pat118_0001/VSD.Brain.XX.O.MR_T1c.35547'

fname_res = os.path.join(sdir, resdir, 'VSD.brats_tcia_pat118_0001.42293.mha')
fname_img = os.path.join(sdir, imgdir, 'VSD.Brain.XX.O.MR_T1c.35547.nii.gz')

res_img = sitk.ReadImage(fname_res)
res_mat = sitk.GetArrayViewFromImage(res_img)

global contour_opacity
contour_opacity = .2
contour_actor = actor.contour_from_roi(res_mat, color=(1, 0, 0), opacity=contour_opacity)

labels_img = nib.load(fname_img)

data_img = labels_img.get_data()

image_actor_z = actor.slicer(data_img)

# Change also the opacity of the slicer
global slicer_opacity
slicer_opacity = .8
image_actor_z.opacity(slicer_opacity)

# 3D image shape
img_shape = data_img.shape

# Add additonal slicers by copying the original and adjusting the ``display_extent``
image_actor_x = image_actor_z.copy()
x_midpoint = int(np.round(img_shape[0] / 2))
image_actor_x.display_extent(x_midpoint, x_midpoint, 0, img_shape[1] - 1, 0, img_shape[2] - 1)

image_actor_y = image_actor_z.copy()
y_midpoint = int(np.round(img_shape[1] / 2))
image_actor_y.display_extent(0, img_shape[0] - 1, y_midpoint, y_midpoint, 0, img_shape[2] - 1)

# Add all the actors to the renderer
r = window.Renderer()
r.add(image_actor_z)
r.add(image_actor_x)
r.add(image_actor_y)
r.add(contour_actor)

show_m = window.ShowManager(r, size=(1200, 900))
show_m.initialize()

z_slider = ui.LineSlider2D(min_value=0, max_value=img_shape[2] - 1, initial_value=img_shape[2] / 2,
                           text_template='{value:.0f}', length=140)

x_slider = ui.LineSlider2D(min_value=0, max_value=img_shape[0] - 1, initial_value=img_shape[0] / 2,
                           text_template='{value:.0f}', length=140)

y_slider = ui.LineSlider2D(min_value=0, max_value=img_shape[1] - 1, initial_value=img_shape[1] / 2,
                           text_template='{value:.0f}', length=140)

slices_opacity_slider = ui.LineSlider2D(min_value=0.0, max_value=1.0, initial_value=slicer_opacity, length=140)

contour_opacity_slider = ui.LineSlider2D(min_value=0.0, max_value=1.0, initial_value=contour_opacity, length=140)


def change_slice_z(slider):
    z = int(np.round(slider.value))
    image_actor_z.display_extent(0, img_shape[0] - 1, 0, img_shape[1] - 1, z, z)


def change_slice_x(slider):
    x = int(np.round(slider.value))
    image_actor_x.display_extent(x, x, 0, img_shape[1] - 1, 0, img_shape[2] - 1)


def change_slice_y(slider):
    y = int(np.round(slider.value))
    image_actor_y.display_extent(0, img_shape[0] - 1, y, y, 0, img_shape[2] - 1)


def change_slices_opacity(slider):
    global slicer_opacity
    slicer_opacity = slider.value
    image_actor_z.opacity(slicer_opacity)
    image_actor_x.opacity(slicer_opacity)
    image_actor_y.opacity(slicer_opacity)


def change_contour_opacity(slider):
    global contour_opacity
    contour_opacity = slider.value
    contour_actor.GetProperty().SetOpacity(contour_opacity)


z_slider.on_change = change_slice_z
x_slider.on_change = change_slice_x
y_slider.on_change = change_slice_y
slices_opacity_slider.on_change = change_slices_opacity
contour_opacity_slider.on_change = change_contour_opacity


def build_label(text):
    label = ui.TextBlock2D()
    label.message = text
    label.font_size = 18
    label.font_family = 'Arial'
    label.justification = 'left'
    label.bold = False
    label.italic = False
    label.shadow = False
    label.background = (0, 0, 0)
    label.color = (1, 1, 1)
    return label


z_label = build_label(text='Z Slice')
x_label = build_label(text='X Slice')
y_label = build_label(text='Y Slice')
slices_opacity_label = build_label(text='Slices Opacity')
contour_opacity_label = build_label(text='Tumor Opacity')

panel = ui.Panel2D(size=(330, 370), color=(1, 1, 1), opacity=0.1, align='right')
panel.center = (1010, 210)

panel.add_element(x_label, (0.05, 0.90))
panel.add_element(x_slider, (0.45, 0.90))
panel.add_element(y_label, (0.05, 0.70))
panel.add_element(y_slider, (0.45, 0.70))
panel.add_element(z_label, (0.05, 0.50))
panel.add_element(z_slider, (0.45, 0.50))
panel.add_element(slices_opacity_label, (0.05, 0.30))
panel.add_element(slices_opacity_slider, (0.45, 0.30))
panel.add_element(contour_opacity_label, (0.05, 0.10))
panel.add_element(contour_opacity_slider, (0.45, 0.10))

show_m.ren.add(panel)

global size
size = r.GetSize()


def win_callback(obj, event):
    global size
    if size != obj.GetSize():
        size_old = size
        size = obj.GetSize()
        size_change = [size[0] - size_old[0], 0]
        panel.re_align(size_change)


show_m.add_window_callback(win_callback)

r.zoom(1.5)
r.reset_clipping_range()

show_m.render()

show_m.start()
