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
from zipfile import ZipFile
import os

from random import randint

if 'key' not in st.session_state:
    st.session_state.key = str(randint(1000, 100000000))

toast = ToastNotifier()
# from utils import FaceMaskDataset, get_transform, get_model, get_device, get_dataloader

PATH = 'FriendDet'

def save_uploadedfile(uploadedfile):
    with open(os.path.join("fileDir",uploadedfile.name),"wb") as f:
        f.write((uploadedfile).getbuffer())
    return st.success("Saved File:{} to fileDir".format(uploadedfile.name))


def load_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return image, width, height
def app():
    #Bulk select option
    zipObj = ZipFile('test.zip', 'w')

    st.title("Upload an Image") 
    options = st.multiselect("Choose which person to download", ["Jun", "Nic"])
    if not options:
        st.error("Please select a person to download")
    else:
        st.write(f"You selected option {options}")

        image = st.file_uploader("Upload an image...", type=["jpg", "png"], key="frienddet", accept_multiple_files=True)
        print(image)
        if image:
            if image is not None:
                try:
                    os.mkdir("fileDir")
                except FileExistsError:
                    print('Directory not created')
                for i in image:

                    img, width, height = load_image(i)
                    img, preds = get_predictions(img, width=width, height=height, PATH=PATH, real_time = False) 
                    print('predicted #boxes: ', preds['labels']) #debugging purposes
                    print('predicted #boxes: ', len(preds['boxes']))
                    
                    print(options)
                    nms_preds = apply_nms(preds, 0.7)
                    image_display, label = plot_img_bbox(torch_to_pil(img), nms_preds, PATH)
                    print(label)
                    if options == ["Jun"]:
                        #apply nms
                        if label == "Jun Mask On" or label == "Jun Mask Off":
                            st.image(image_display, 50)
                            save_uploadedfile(i)
                            #if equals to name
                            zipObj.write(f'fileDir/{i.name}')
                            print("Saved!")

                    elif options == ["Nic"]:
                        if label == "Nic Mask On" or label == "Nic Mask Off":
                            st.image(image_display, width=50)
                            
                            save_uploadedfile(i)
                            #if equals to name
                            zipObj.write(f'fileDir/{i.name}')
                            print("Saved!")

                    elif options == ["Nic", "Jun"] or ["Jun, Nic"]:
                        if label == "Nic Mask On" and label == "Nic Mask Off" and label == "Jun Mask On" and label == "Jun Mask Off":
                            st.image(image_display, width=50)
                            save_uploadedfile(i)
                            #if equals to name
                            zipObj.write(f'fileDir/{i.name}')
                            print("Saved!")

                
            zipObj.close()
            with open("test.zip", "rb") as fp:
                if st.download_button("Download images of friends!", data=fp, file_name="test.zip", mime="application/zip"):
                    st.session_state.key = str(randint(1000, 100000000))
                    st.sync()
            
            
                
                # if label == 'Without Mask':
                #     toast.show_toast("Face Masked Alert","Please wear your mask!",duration=20,icon_path="Face-Mask.ico")
                # elif  label == 'Mask Weared Incorrect':
                #     toast.show_toast("Face Masked Alert","Wear your mask properly!",duration=20,icon_path="Face-Mask.ico")
                

