import cv2
from PIL import Image
from pdf2image import convert_from_path
import numpy as np

def convert_pdf_to_ssp_format(input_pdf_path, output_pdf_path):
    # Convert first page of PDF to image
    pages = convert_from_path(input_pdf_path)
    image_path = input_pdf_path.replace('.pdf', '.jpg')
    pages[0].save(image_path, 'JPEG')
    
    img = cv2.imread(image_path)

    # Remove text at fixed position (based on SSP layout)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, (180, 720), (1000, 765), 255, -1)
    img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    # Insert hologram from fixed SSD image
    ssd_path = 'static/output/ssd_reference.jpg'
    ssd = cv2.imread(ssd_path)
    hologram = ssd[360:450, 615:745]  # Crop region from SSD

    # Paste hologram into cleaned image (based on SSP placement)
    img[720:810, 870:1000] = hologram

    # Save processed image and convert to PDF
    result_image_path = input_pdf_path.replace('.pdf', '_processed.jpg')
    cv2.imwrite(result_image_path, img)
    image = Image.open(result_image_path)
    image.save(output_pdf_path, "PDF", resolution=100.0)
