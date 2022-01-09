import streamlit as st
from PIL import Image
import matplotlib
matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plt
import matplotlib.patches as patches
#Opencv and torch utils
import cv2
import torch
from faster_utils import FaceMaskDataset, get_predictions, get_model_instance_segmentation, torch_to_pil, plot_img_bbox, apply_nms
from win10toast import ToastNotifier
toast = ToastNotifier()
# from utils import FaceMaskDataset, get_transform, get_model, get_device, get_dataloader
def load_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return image, width, height
def app():
    
    st.title("Upload an Image") 
    image = st.file_uploader("Upload an image...", type=["jpg"], key="frienddet")
    if image:
        if image is not None:
            # file_details = {"FileName":image.name,"FileType":image.type,"FileSize":image.size}
            # st.write(file_details)

            img, width, height = load_image(image)
            img, preds = get_predictions(img, width=width, height=height, real_time = False) 
            print('predicted #boxes: ', preds['labels']) #debugging purposes
            print('predicted #boxes: ', len(preds['boxes']))
            #apply nms
            nms_preds = apply_nms(preds, 0.7)
            # print('real #boxes: ', len(target['labels']))
            image_display, label = plot_img_bbox(torch_to_pil(img), nms_preds)
            st.image(image_display)
            
            if label == 'Without Mask':
                toast.show_toast("Face Masked Alert","Please wear your mask!",duration=20,icon_path="Face-Mask.ico")
            elif  label == 'Mask Weared Incorrect':
                toast.show_toast("Face Masked Alert","Wear your mask properly!",duration=20,icon_path="Face-Mask.ico")
            
            # FRAME_WINDOW = st.image([])
            # FRAME_WINDOW.image(image)
