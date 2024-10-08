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

# function that searches for perks in the end screen given the end screen image and positions of the ROIs
def search(end_screen, always_dejavu):
    end_screen_gray=cv2.cvtColor(end_screen, cv2.COLOR_BGR2GRAY) # convert the image to grayscale to allow for thresholding
    rois = [
        (158 + (j*47), 343 + (i*102), 42, 42)  # (x (top left), y (top left), width, height)

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
    #  resize reference images so they match the size of the ROIs (47x47), otherwise the program will error out
    resized_reference_images = [
        cv2.resize(cv2.imread(os.path.join('assets/perks', file_name), cv2.IMREAD_GRAYSCALE), (42, 42))
        for file_name in reference_files
    ]
    recognised_perks = [] 
    # main loop to iterate through all ROIs
    for i, (x, y, w, h) in enumerate(rois):
        roi = end_screen_gray[y:y+h, x:x+w]
        #cv2.imwrite('testing/tests/roi'+str(i)+'.png', roi) # save the ROIs for testing 
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