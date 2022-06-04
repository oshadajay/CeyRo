# CeyRo Traffic Sign and Traffic Light Dataset

![classes_grid](https://github.com/oshadajay/CeyRo/blob/main/figures/classes_grid.png)

## Overview

CeyRo is a novel benchmark dataset for traffic sign and traffic light detection which covers a wide variety of challenging urban, sub-urban and rural road scenarios in Sri Lanka. 
The dataset consists of 7984 total images of 1920 &times; 1080 resolution with 10176 traffic sign and traffic light instances belonging to 70 traffic sign and 5 traffic light classes. 

For more details, please refer to our paper [Towards Real-time Traffic Sign and Traffic Light Detection on Embedded Systems](https://arxiv.org/abs/2205.02421).

## Download

The train set, the test set and a sample of the CeyRo traffic sign and traffic light dataset can be downloaded from the following Google Drive links.
* [Train Set](https://drive.google.com/file/d/105J3fU3G_ujxNCFp9KX3u_PnbGcCkhXa/) - 6143 images (3.64 GB)
* [Test Set](https://drive.google.com/file/d/1MHqePR3ShjCh6GdpUKHbFpGyMztqAR6A/) - 1841 images (1.1 GB)
* [Sample](https://drive.google.com/file/d/1DIZWkK2qsnZ113zy3ESlUA68q937z6-G/) - 10 images (6 MB)

## Annotations

The traffic sign and traffic light annotations are provided as bounding boxes in the PASCAL VOC format.
[LabelImg](https://github.com/tzutalin/labelImg) can be used to visualize the bounding box annotations (Images and XML files should be copied to the same folder).

![annotation_format](https://github.com/oshadajay/CeyRo/blob/main/figures/annotation_format.png)

## Statistics

The number of traffic sign and traffic light instances present in each superclass is listed in the below table.

| Superclass | Train | Test | Total |
|----------|:------------------:|:-----------------:|:----------------------:|
|Danger Warning Signs (DWS) |2833 |809 |3642|
|Mandatory Signs (MNS) |453 |128 |581|
|Prohibitory Signs (PHS) |650 |195 |845|
|Priority Signs (PRS) |115 |26 |141|
|Speed Limit Signs (SLS) |735 |237 |972|
|Other Signs Useful for Drivers (OSD) |1619| 498| 2117|
|Additional Regulatory Signs (APR) |377 |123 |500|
|Traffic Light Signs (TLS) |1075| 303 |1378|
|Total |7857 |2319| 10176|

## Evaluation

To be updated.

## Citation

If you use our dataset in your work, please cite the following paper.
```
@article{jayasinghe2022towards,
  title={Towards Real-time Traffic Sign and Traffic Light Detection on Embedded Systems},
  author={Jayasinghe, Oshada and Hemachandra, Sahan and Anhettigama, Damith and Kariyawasam, Shenali and Wickremasinghe, Tharindu and Ekanayake, Chalani and Rodrigo, Ranga and Jayasekara, Peshala},
  journal={arXiv preprint arXiv:2205.02421},
  year={2022}
}
```