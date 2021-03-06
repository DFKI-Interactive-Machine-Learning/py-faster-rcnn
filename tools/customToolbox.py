"""
    py-faster-rcnn-ft - Custom Training of Deep Learning Models for Image Classification
    Copyright (C) 2017  DFKI GmbH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import sys
import os

pylab.rcParams['figure.figsize'] = (10.0, 8.0)

rootPath = '../data/coco'
annPath = 'annotations'
dataType = 'train2014'
annFile = '%s/%s/instances_%s.json'%(rootPath, annPath, dataType)


def create_class_tuple(cat_ids=[]):
    """Creates a tuple containing the string representation for the given category IDs. Call this method to
    specify the classes in demo.py"""
    coco = COCO(annFile)

    result_list = ['__background__']

    if len(cat_ids) == 0:
        categories = coco.loadCats(coco.getCatIds())
    else:
        categories = coco.loadCats(cat_ids)

    for index, item in enumerate(categories):
        cat_string = categories[index].get('name')

        result_list.append(cat_string)

    return tuple(result_list)


def show_val_images(cat_ids):
    """Shows one random image from the validation set for the given category id"""

    val_annFile = '%s/%s/instances_%s.json' % (rootPath, annPath, "minival2014")
    coco = COCO(val_annFile)

    imgIds = coco.getImgIds(catIds=cat_ids)

    img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]
    image_path = "../data/coco/images/val2014/" + str(img['file_name'])
    print "file: {}".format(image_path)

    categories = coco.loadCats(cat_ids)
    print "categories : "
    for item in categories:
        print str(item['name'])

    I = io.imread(image_path)
    plt.figure()
    plt.axis('off')
    plt.imshow(I)
    annIds = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
    anns = coco.loadAnns(annIds)
    coco.showAnns(anns)
    plt.show()


def get_val_images(amount, cat_ids):
    """Loads random image paths from the validation set for the given category Ids"""

    val_annFile = '%s/%s/instances_%s.json' % (rootPath, annPath, "minival2014")
    coco = COCO(val_annFile)

    cat_names = []

    if len(cat_ids) == 0:
        categories = coco.loadCats(coco.getCatIds())
    else:
        categories = coco.loadCats(cat_ids)

    for item in categories:
        cat_names.append(str(item['name']))

    path_list = []

    for index, cur_cat_id in enumerate(cat_ids):

        print "\n--- Images for category {} ---".format(cat_names[index])
        imgIds = coco.getImgIds(catIds=cur_cat_id)

        for i in range(amount):
            img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]
            image_path = "../data/coco/images/val2014/" + str(img['file_name'])
            print image_path
            path_list.append(image_path)

    print "\nLoaded {} for the categories {}\n".format(str(amount), str(cat_names))

    return path_list


def get_category_images(cat_ids, annotation_path="../data/coco/annotations/instances_minival2014.json", image_folder_path="", print_file_names=True):
    """
    Returns a dictionary containing all image file names from the given annotation with the defined category id.
    :param cat_ids: list of category ids with which the returned image paths should be labeled with
    :param annotation_path: path of the .json file containing the image annotations
    :param image_folder_path: file path of the folder containing all image data (dataset) - optional
    :param print_file_names: if True, all found file names will be printed additionally to the console
    :return: dictionary of the shape: dict[category id] = <list of image file names>
    """

    # check if file exists
    if not os.path.isfile(annotation_path):
        print("{} is not a valid file. Please check the file path".format(annotation_path))
        assert False

    # check if the file is a json file
    if not annotation_path.lower().endswith('.json'):
        print("Annotation files have to in json format!")
        assert False

    val_annFile = annotation_path
    coco = COCO(val_annFile)

    cat_names = []

    if len(cat_ids) == 0:
        categories = coco.loadCats(coco.getCatIds())
    else:
        categories = coco.loadCats(cat_ids)

    for item in categories:
        cat_names.append(str(item['name']))

    image_dict = {}

    for index, cur_cat_id in enumerate(cat_ids):

        image_dict[cur_cat_id] = []

        if print_file_names:
            print "\n--- Images for category {} ---".format(cat_names[index])

        # ids of all images that belong to the cat id
        imgIds = coco.getImgIds(catIds=cur_cat_id)
        imgs = coco.loadImgs(imgIds)

        for img in imgs:

            if len(image_folder_path) > 0:
                image_path = image_folder_path + "/" + str(img['file_name'])
            else:
                image_path = str(img['file_name'])

            if print_file_names:
                print image_path

            image_dict[cur_cat_id].append(image_path)

        print "\nLoaded {} images for the category {}\n".format(str(len(imgs)), str(cat_names[index]))

    return image_dict


if __name__ == '__main__':
    # show_val_images([3])
    get_category_images([3])
