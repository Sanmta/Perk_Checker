import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim

# function to compute mean squared error (MSE) between two images (average squared difference per pixel)
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

# function that compares two images using MSE and SSIM values
def compare_images(imageA, imageB):
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    return m, s

def switch(ui_scale):
    switcher = {
        70: 37,
        75: 39,
        80: 42,
        85: 44,
        90: 46,
        95: 49,
        100: 50
        }
    return switcher.get(ui_scale)

# function that searches for perks in the end screen given the end screen image and positions of the ROIs
def search(end_screen, always_dejavu, ui_scale):
    end_screen_gray=cv2.cvtColor(end_screen, cv2.COLOR_BGR2GRAY) # convert the image to grayscale to allow for thresholding
    widths = switch(ui_scale) # get the width of the ROIs based on the UI scale
    if ui_scale == 70:
        rois = [
            (129 + (j*38), 372 + (i*85), widths, widths)  # (x (top left), y (top left), width, height)

            for i in range(4)  # builds
            for j in range(4)  # perks
        ]
    elif ui_scale == 75:
        rois = [
            (137 + (j*43), 360 + (i*91), widths, widths)  # (x (top left), y (top left), width, height)

            for i in range(4)  # builds
            for j in range(4)  # perks
        ]
    elif ui_scale == 80:
        rois = [
            (148 + (j*43), 348 + (i*97), widths, widths)  # (x (top left), y (top left), width, height)

            for i in range(4)  # builds
            for j in range(4)  # perks
        ]
    elif ui_scale == 85:
        rois = [
            (157 + (j*47), 336 + (i*103), widths, widths)  # (x (top left), y (top left), width, height)

            for i in range(4)  # builds
            for j in range(4)  # perks
        ]
    elif ui_scale == 90:
        rois = [
            (167 + (j*50), 325 + (i*107), widths, widths)  # (x (top left), y (top left), width, height)

            for i in range(4)  # builds
            for j in range(4)  # perks
        ]
    elif ui_scale == 95:
        rois = [
            (175 + (j*53), 313 + (i*115), widths, widths)  # (x (top left), y (top left), width, height)

            for i in range(4)  # builds
            for j in range(4)  # perks
        ]
    elif ui_scale == 100:
        rois = [
            (185 + (j*56), 301 + (i*121), widths, widths)  # (x (top left), y (top left), width, height)

            for i in range(4)  # builds
            for j in range(4)  # perks
        ]
    # performed testing with standard pngs, then with pngs along with perk backgrounds, however the accuracy was low
    # so switched to jpgs with solid white background, which provided a higher accuracy
    reference_files = os.listdir('assets/perks') 
    reference_images = [
        cv2.imread(os.path.join('assets/perks', file_name), cv2.IMREAD_GRAYSCALE) # load reference images in grayscale
        for file_name in reference_files
    ]
    #  resize reference images so they match the size of the ROIs, otherwise the program will error out
    resized_reference_images = [
        cv2.resize(cv2.imread(os.path.join('assets/perks', file_name), cv2.IMREAD_GRAYSCALE), (widths, widths))
        for file_name in reference_files
    ]
    recognised_perks = [] 
    # main loop to iterate through all ROIs
    for i, (x, y, w, h) in enumerate(rois):
        roi = end_screen_gray[y:y+h, x:x+w]
        cv2.imwrite('testing/tests/roi'+str(i)+'.png', roi) # save the ROIs for testing 
        _, thresholded_roi = cv2.threshold(roi, 106, 255, cv2.THRESH_BINARY) # apply thresholding in case needed
        mse_result = 0  # CURRENTLY UNUSED FOR COPARISON BUT HERE IN CASE NEEDED LATER #
        ssim_result = 0
        for j, reference_image in enumerate(resized_reference_images):
            threshold_needed = False # flag to indicate if thresholding is needed (essentially, "is it an eye perk?")
            m, s = compare_images(roi, reference_image)
            # higher SSIM value indicates a better match
            if s > ssim_result:
                mse_result = m
                ssim_result = s
                best_match = j

        # if the best match is an eye perk, apply thresholding to the ROI and compare again as they are harder to match
        if "DejaVu" in reference_files[best_match] or "ObjectOfObsession" in reference_files[best_match] or "DarkSense" in reference_files[best_match] or "Kindred" in reference_files[best_match]:
            threshold_needed = True # flag to indicate that thresholding is needed
            if (always_dejavu == True):
                for p, perk in enumerate(reference_files):
                    if "DejaVu" in perk:
                        best_match_threshold = p
                        break
            else:    
                ssim_result_threshold = 0
                mse_result_threshold = 0
                for k, reference_image in enumerate(resized_reference_images):
                    n, r = compare_images(thresholded_roi, reference_image) 
                    # higher SSIM value still indicates a better match, pretty much every time the eye perk will be deja vu, so if I
                    # run into issues identifying the perk in the future, I can just hardcode it to be deja vu
                    if r > ssim_result_threshold:
                        mse_result_threshold = n
                        ssim_result_threshold = r
                        best_match_threshold = k
        if threshold_needed == True:
           recognised_perks.insert(i, reference_files[best_match_threshold])
        else: 
            recognised_perks.insert(i, reference_files[best_match])    
    return recognised_perks
        
if __name__ == '__main__':
    search()