'''
Evaluation script for the CeyRo Traffic Sign and Traffic Light Dataset
gt_dir should contain the ground truth xml files and pred_dir should contain prediction xml files respectively.
The file system should follow the following order.
home_directory/
|___ gt_dir/
|      |___001.xml
|      |___002.xml
|      |___ ....
|___ pred_dir/
       |___001.xml
       |___002.xml
       |___ ....
'''

from shapely.geometry import Polygon
from tabulate import tabulate
from os import listdir
from xml.etree import ElementTree as ET
import argparse

class_dict = {"DWS-01": 0, "DWS-02": 0, "DWS-03": 0, "DWS-04": 0, "DWS-09": 0, "DWS-10": 0, "DWS-11": 0, 
              "DWS-12": 0, "DWS-13": 0, "DWS-14": 0, "DWS-15": 0, "DWS-16": 0, "DWS-17": 0, "DWS-18": 0, 
              "DWS-19": 0, "DWS-20": 0, "DWS-21": 0, "DWS-25": 0, "DWS-26": 0, "DWS-27": 0, "DWS-28": 0, 
              "DWS-29": 0, "DWS-32": 0, "DWS-33": 0, "DWS-35": 0, "DWS-36": 0, "DWS-40": 0, "DWS-41": 0, 
              "DWS-42": 0, "DWS-44": 0, "DWS-46": 0, "MNS-01": 0, "MNS-02": 0, "MNS-03": 0, "MNS-04": 0, 
              "MNS-05": 0, "MNS-06": 0, "MNS-07": 0, "MNS-09": 0, "OSD-01": 0, "OSD-02": 0, "OSD-03": 0, 
              "OSD-04": 0, "OSD-06": 0, "OSD-07": 0, "OSD-16": 0, "OSD-17": 0, "OSD-26": 0, "PHS-01": 0, 
              "PHS-02": 0, "PHS-03": 0, "PHS-04": 0, "PHS-09": 0, "PHS-23": 0, "PHS-24": 0, "PRS-01": 0, 
              "PRS-02": 0, "RSS-02": 0, "SLS-100": 0, "SLS-15": 0, "SLS-40": 0, "SLS-50": 0, "SLS-60": 0, 
              "SLS-70": 0, "SLS-80": 0, "APR-09": 0, "APR-10": 0, "APR-11": 0, "APR-12": 0, "APR-14": 0, 
              "TLS-C": 0, "TLS-E": 0, "TLS-G": 0, "TLS-R": 0, "TLS-Y":0}

def get_bboxes(filename):

    bboxes = []

    tree = ET.parse(filename)
    root = tree.getroot()

    for child in root:
        if(child.tag == 'object'):
            bbox = {'label':None, "points":None}
            for grandChild in child:
                if(grandChild.tag == 'bndbox'):
                    for coor in grandChild:
                        if(coor.tag == 'xmin'): x1 = int(coor.text)
                        if(coor.tag == 'ymin'): y1 = int(coor.text)
                        if(coor.tag == 'xmax'): x2 = int(coor.text)
                        if(coor.tag == 'ymax'): y2 = int(coor.text)

                if(grandChild.tag == 'name'):
                    label = grandChild.text

            bbox['label'] = label
            bbox['points'] = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
            bboxes.append(bbox)

    return bboxes

def get_IoU(pol_1, pol_2):

    # Define each polygon
    polygon1_shape = Polygon(pol_1)
    polygon2_shape = Polygon(pol_2)

    if ~(polygon1_shape.is_valid):polygon1_shape = polygon1_shape.buffer(0)
    if ~(polygon2_shape.is_valid):polygon2_shape = polygon2_shape.buffer(0)

    # Calculate intersection and union, and return IoU
    polygon_intersection    = polygon1_shape.intersection(polygon2_shape).area
    polygon_union           = polygon1_shape.area + polygon2_shape.area - polygon_intersection

    return polygon_intersection / polygon_union

def match_gt_with_pred(gt_bboxes, pred_bboxes, iou_threshold):

    candidate_dict_gt  = {}  
    assigned_predictions = []

    # Iterate over ground truth
    for idx_gt, gt_itm in enumerate(gt_bboxes):
        pts_gt       = gt_itm['points']
        label_gt     = gt_itm['label']
        gt_candidate = {'label_pred':None, 'iou':0}
        assigned_prediction = None

        # Iterate over predictions
        for idx_pred, pred_itm in enumerate(pred_bboxes):
            pts_pred   = pred_itm['points']
            label_pred = pred_itm['label']
            iou        = get_IoU(pts_pred, pts_gt)

            # Match gt with predicitons
            if (iou > iou_threshold) and (gt_candidate['iou'] < iou) and (label_gt == label_pred) and str(idx_pred) not in assigned_predictions:
                gt_candidate['label_pred'] = label_pred + '*' + str(idx_pred)
                gt_candidate['iou']        = iou
                assigned_prediction        = str(idx_pred)

        if assigned_prediction is not None:
            assigned_predictions.append(assigned_prediction)

        candidate_dict_gt[label_gt + '*' + str(idx_gt)] = gt_candidate

    return candidate_dict_gt

def eval_detections(gt_dir, pred_dir, iou_threshold = 0.3):

    gt_xml_count   = len([f for f in listdir(gt_dir) if f.endswith('.xml')])
    pred_xml_count = len([f for f in listdir(pred_dir) if f.endswith('.xml')])

    assert gt_xml_count == pred_xml_count, "Ground truth xml file count does not match with prediction xml file count"

    print("Evaluating traffic sign and traffic light detection performance on " + str(gt_xml_count) + " files")
    print()

    classwise_results    = [['Class', 'Precision', 'Recall', 'F1_Score']]

    filenames = [f for f in listdir(gt_dir) if f.endswith('.xml')]

    sigma_tp = 0
    sigma_fp = 0
    sigma_fn = 0

    tp_class_dict   = class_dict.copy()
    gt_class_dict   = class_dict.copy()
    pred_class_dict = class_dict.copy()

    # Iterate over each file
    for file in filenames:
        # Load ground truth xml file
        gt_bboxes   = get_bboxes((gt_dir + '/' + file))
        # Load pred xml file
        pred_bboxes = get_bboxes((pred_dir + '/' + file))

        for bbox in gt_bboxes:
            gt_class_dict[bbox['label']]  += 1

        for bbox in pred_bboxes:
            pred_class_dict[bbox['label']]  += 1

        tp_gt = 0

        candidate_dict_gt = match_gt_with_pred(gt_bboxes, pred_bboxes, iou_threshold)

        for idx, lab in enumerate(candidate_dict_gt):
            label    = lab.split('*')[0]
            pred_lab = candidate_dict_gt[lab]['label_pred']

            if pred_lab != None:
                tp_gt                      += 1
                tp_class_dict[label]       += 1

        tp = tp_gt
        fp = len(pred_bboxes) - tp
        fn = len(gt_bboxes) - tp

        sigma_tp += tp
        sigma_fp += fp
        sigma_fn += fn

    # Calculate precision, recall and F1 for the whole dataset
    if (sigma_tp + sigma_fp) != 0:
        precision = sigma_tp / (sigma_tp + sigma_fp)
    else:
        precision = 0

    if (sigma_tp + sigma_fn) != 0:
        recall = sigma_tp / (sigma_tp + sigma_fn)
    else:
        recall = 0

    if (precision + recall) != 0:
        F1_score = (2 * precision * recall) / (precision + recall)
    else:
        F1_score = 0

    # Calculate class-wise performance metrics
    for label in tp_class_dict:
        l_tp = tp_class_dict[label]
        l_fp = pred_class_dict[label] - l_tp
        l_fn = gt_class_dict[label] - l_tp

        if (l_tp + l_fp) != 0:
            l_precision = l_tp / (l_tp + l_fp)
        else:
            l_precision = 0

        if (l_tp + l_fn) != 0:
            l_recall = l_tp / (l_tp + l_fn)
        else:
            l_recall = 0

        if (l_precision + l_recall) != 0:
            l_F1_score = (2 * l_precision * l_recall) / (l_precision + l_recall)
        else:
            l_F1_score = 0

        if gt_class_dict[label] != 0:
            classwise_results.append([label, round(l_precision, 4), round(l_recall, 4), round(l_F1_score, 4)])

    print('Class-wise traffic sign and traffic light detection results')
    print(tabulate(classwise_results, headers='firstrow', tablefmt='grid'))
    print()

    print("Overall Precision : " + str(round(precision, 4)))
    print("Overall Recall    : " + str(round(recall, 4)))
    print("Overall F1-Score  : " + str(round(F1_score, 4)))

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gt_dir', type = str, help = 'Filepath containing ground truth xml files')
    parser.add_argument('--pred_dir', type = str, help = 'Filepath containing prediction xml files')
    parser.add_argument('--iou_threshold', type = float, default = 0.3, help = 'IoU threshold to count a prediction as a true positive')
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = parse_opt()
    eval_detections(opt.gt_dir, opt.pred_dir, opt.iou_threshold)