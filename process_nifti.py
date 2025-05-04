from config import *
from models import *
import nibabel as nib
import numpy as np
from tqdm import tqdm
from cv2 import resize, INTER_NEAREST
import os
from argparse import ArgumentParser


def process_nifti_file(input_path, output_path):
    input_img = nib.load(input_path)
    input_data = input_img.get_fdata()

    model = get_deepseg_model(
        encoder_name=config['encoder_name'],
        decoder_name=config['decoder_name'],
        n_classes=config['n_classes'],
        input_height=config['input_height'],
        input_width=config['input_width'],
        depth=config['model_depth'],
        filter_size=config['filter_size'],
        up_layer=config['up_layer'],
        trainable=config['trainable'],
        load_model=config['load_model']
    )

    pred_data = np.zeros(input_data.shape)

    for n in tqdm(range(input_data.shape[2])):
        tmp_input = np.zeros((input_data.shape[0], input_data.shape[1], 3))
        for ch in range(3):
            tmp_input[:, :, ch] = input_data[:, :, n]

        tmp_input = resize(tmp_input, (224, 224), interpolation=INTER_NEAREST)
        tmp_input = tmp_input.reshape(1, 224, 224, 3)

        tmp_input = (tmp_input / tmp_input.max()) * 255
        tmp_input = tmp_input.astype(np.uint8)

        img_mean = tmp_input.mean()
        img_std = tmp_input.std()
        if img_std != 0:
            tmp_input = (tmp_input - img_mean) / img_std
        else:
            tmp_input = tmp_input - img_mean

        pr = model.predict(tmp_input)[0]
        pr = pr.reshape((config['output_height'], config['output_width'], config['n_classes'])).argmax(axis=2)

        pred_data[:, :, n] = resize(pr, (input_data.shape[0], input_data.shape[1]), interpolation=INTER_NEAREST)

    input_img.header.set_data_dtype(np.uint8)
    pred_data = pred_data.astype(np.uint8)
    pred_img = nib.Nifti1Image(pred_data, input_img.affine, input_img.header)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    nib.save(pred_img, output_path)
    print(f"Result saved in {output_path}")


if __name__ == "__main__":
    parser = ArgumentParser(description='Processing with DeepSeg')
    parser.add_argument('--i', help='Input NIfTI file path')
    parser.add_argument('--o', help='File for saving segmented NIfTI')

    args = parser.parse_args()

    process_nifti_file(args.i, args.o)
