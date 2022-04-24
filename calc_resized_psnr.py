import numpy as np
import os
from PIL import Image

def calc_psnr(img1, img2, max_value):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        mse = 1e-9
        # return float('inf')
    return 20. * np.log10(max_value / np.sqrt(mse))

pred_dir = './NAFNet-GoPro-width64-visual'
gt_dir = './GoPro-GT'

pred_files = sorted(os.listdir(pred_dir))
gt_files = sorted(os.listdir(gt_dir))

psnrs = []

cnt = 0
total_cnt = len(gt_files)

resize_h = 256
resize_w = 256

assert len(pred_files) == len(gt_files)
for pred_file, gt_file in zip(pred_files, gt_files):
    cnt += 1

    if cnt % 50 == 0:
        print(f'{cnt}/{total_cnt}')

    pred = Image.open(os.path.join(pred_dir, pred_file)).resize((resize_w, resize_h))
    gt = Image.open(os.path.join(gt_dir, gt_file)).resize((resize_w, resize_h))

    #720x1280x3 by default

    pred = np.array(pred).astype(np.float64)
    gt = np.array(gt).astype(np.float64)

    psnr = calc_psnr(pred, gt, 255.)
    psnrs.append(psnr)

    print(psnr)


print(f'psnr final {np.mean(psnrs)}.. resize: ({resize_h},{resize_w})')

