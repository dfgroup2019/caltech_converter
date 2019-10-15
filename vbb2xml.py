import os, glob
import cv2
from scipy.io import loadmat
from collections import defaultdict
import numpy as np
from lxml import etree, objectify
import time

def vbb_anno2dict(vbb_file, cam_id):
    #通过os.path.basename获得路径的最后部分“文件名.扩展名”
    #通过os.path.splitext获得文件名
    filename = os.path.splitext(os.path.basename(vbb_file))[0]

    #定义字典对象annos
    annos = defaultdict(dict)
    vbb = loadmat(vbb_file)
    # object info in each frame: id, pos, occlusion, lock, posv
    objLists = vbb['A'][0][0][1][0]
    objLbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]     #可查看所有类别        
    # person index
    person_index_list = np.where(np.array(objLbl) == "person")[0]   #只选取类别为‘person’的xml
    for frame_id, obj in enumerate(objLists):
        if len(obj) > 0:
            frame_name = str(cam_id) + "_" + str(filename) + "_" + str(frame_id+1) + ".jpg"
            annos[frame_name] = defaultdict(list)
            annos[frame_name]["id"] = frame_name
            annos[frame_name]["label"] = "person"
            for id, pos, occl in zip(obj['id'][0], obj['pos'][0], obj['occl'][0]):
                id = int(id[0][0]) - 1  # for matlab start from 1 not 0
                if not id in person_index_list:  # only use bbox whose label is person
                    continue
                pos = pos[0].tolist()
                occl = int(occl[0][0])
                annos[frame_name]["occlusion"].append(occl)
                annos[frame_name]["bbox"].append(pos)
            if not annos[frame_name]["bbox"]:
                del annos[frame_name]

    # print (annos)
    return annos


#根据anno生成对应的xml树
def instance2xml_base(anno, bbox_type='xyxy'):
    """bbox_type: xyxy (xmin, ymin, xmax, ymax); xywh (xmin, ymin, width, height)"""
    assert bbox_type in ['xyxy', 'xywh']
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('VOC2014_instance/person'),
        E.filename(anno['id']),
        E.source(
            E.database('Caltech pedestrian'),
            E.annotation('Caltech pedestrian'),
            E.image('Caltech pedestrian'),
            E.url('None')
        ),
        E.size(
            E.width(640),
            E.height(480),
            E.depth(3)
        ),
        E.segmented(0),
    )
    for index, bbox in enumerate(anno['bbox']):
        bbox = [float(x) for x in bbox]
        if bbox_type == 'xyxy':
            xmin, ymin, w, h = bbox
            xmax = xmin+w
            ymax = ymin+h
        else:
            xmin, ymin, xmax, ymax = bbox
        # print(xmin, ymin, xmax, ymax)
        if xmin<0:
            xmin=0
        if xmax >640:
            xmax = 640
        if ymin<0:
            ymin=0
        if ymax>480:
            ymax=480
        # assert not (xmin<0 or ymin<0 or xmax>640 or ymax>480)
        E = objectify.ElementMaker(annotate=False)
        anno_tree.append(
            E.object(
            E.name(anno['label']),
            E.bndbox(
                E.xmin(xmin),
                E.ymin(ymin),
                E.xmax(xmax),
                E.ymax(ymax)
            ),
            E.difficult(0),
            E.occlusion(anno["occlusion"][index])
            )
        )
    return anno_tree


def parse_anno_file(vbb_inputdir,vbb_outputdir):
    # annotation sub-directories in hda annotation input directory
    assert os.path.exists(vbb_inputdir)
    if not os.path.exists(vbb_outputdir):
        os.makedirs(vbb_outputdir)
    #每个set对应一个camera,每个camera对应多个vedio,即v000
    for set_dir in os.listdir(vbb_inputdir): #对应set00,set01...
        for vbb_file in glob.glob(os.path.join(vbb_inputdir, set_dir, "*.vbb")):
            print(vbb_file)
            #每一帧(filename)对应的参数，最重要的是坐标
            annos = vbb_anno2dict(vbb_file, set_dir)
            
            if annos:
                #filename ~ set00_v001_1.jpg
                for filename, anno in sorted(annos.items(), key=lambda x: x[0]):                  
                    if "bbox" in anno:
                        anno_tree = instance2xml_base(anno)
                        foldername = os.path.splitext(vbb_file[0])
                        new_output_dir = os.path.join(vbb_outputdir,set_dir)                        
                        folder = os.path.exists(new_output_dir)
                        
                        if not folder:
                            os.mkdir(new_output_dir)
                            
                        vbb_file_name = os.path.basename(vbb_file)
                        new_output_dir2 = os.path.join(new_output_dir,vbb_file_name)
                        folder2 = os.path.exists(new_output_dir2)
                        if not folder2:
                            os.mkdir(new_output_dir2)
                        outfile = os.path.join(new_output_dir2, os.path.splitext(filename)[0]+".xml")
                        # print ("Generating annotation xml file of picture: ", filename)
                        #生成最终的xml文件，对应一张图片
                        etree.ElementTree(anno_tree).write(outfile, pretty_print=True)

def main():
    vbb_inputdir = 'E:\\traffic participant\\caltech_data\\annotations'
    #assert os.path.exists(vbb_inputdir)
    vbb_outputdir = 'E:\\traffic participant\\caltech_data\\vbb2xml'

    start = time.time()
    parse_anno_file(vbb_inputdir,vbb_outputdir)
    end = time.time()

    print('Time taken : {} seconds'.format(end-start))

if __name__ == "__main__":
    main()
