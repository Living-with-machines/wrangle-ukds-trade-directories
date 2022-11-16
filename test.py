import detectron2
import layoutparser as lp
from cv2 import imread

print("is_detectron2_available", lp.is_detectron2_available())

image = imread(
    "./files/UKDS_Versions/UKDA-5101-txt/txt/bcl15027/tiff/0001_bcl15027_tif_00009zo0.tif"
)

model = lp.Detectron2LayoutModel(
    config_path="lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config",
    label_map={
        1: "Page Frame",
        2: "Row",
        3: "Title Region",
        4: "Text Region",
        5: "Title",
        6: "Subtitle",
        7: "Other",
    },
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
)

print(model.detect(image))
