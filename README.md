### Fork of py-faster-rcnn
We forked the original version of [py-faster-rcnn](https://github.com/rbgirshick/py-faster-rcnn) for adding changes relevant to our research. For quick introduction/license/etc. please see the original version of [py-faster-rcnn](https://github.com/rbgirshick/py-faster-rcnn).

The changes were concerned about fine-tuning deep neural networks:
* automated change of network-layers if less classes are considered compared to the original network
* more convenient selection of training classes from ms coco


### Contents
1. [Requirements: software](#requirements-software)
2. [Requirements: hardware](#requirements-hardware)
3. [Basic installation](#installation-sufficient-for-the-demo)
4. [Demo](#demo)
5. [Beyond the demo: training and testing VOC](#beyond-the-demo-installation-for-training-and-testing-models-for-voc)
6. [Beyond the demo: training and testing MSCOCO](#beyond-the-demo-installation-for-training-and-testing-models-for-mscoco)
7. [Available Classes to Train On (MSCOCO)](#available-classes-to-train-on-mscoco)
8. [Train on custom classes](#train-on-custom-classes)
9. [Usage](#usage)

### Requirements: software

1. Requirements for  `Caffe` and `pycaffe` (see: [Caffe installation instructions](http://caffe.berkeleyvision.org/installation.html))

  **Note:** You don't need to install pycaffe separately, we have included pycaffe in our repository with small changes needed for our research. Just check if you have necessary libraries for installing pycaffe 
  
  **Note:** Caffe *must* be built with support for Python layers!

  ```make
  # In your Makefile.config, make sure to have this line uncommented
  WITH_PYTHON_LAYER := 1
  # Unrelatedly, it's also recommended that you use CUDNN
  USE_CUDNN := 1

  # USE_PKG_CONFIG to produce necessary paths for libraries like opencv etc.
  USE_PKG_CONFIG := 1

  # If you use Ubuntu you also need to include the library hdf5
  INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial

  # If you have installed OpenCV Version 3 you need to uncomment the following line:
  OPENCV_VERSION := 3
  ```



  You can download my [Makefile.config](https://dl.dropboxusercontent.com/s/6joa55k64xo2h68/Makefile.config?dl=0) for reference.
2. Python packages you might not have: `cython`, `python-opencv`, `easydict`

3. [Optional] MATLAB is required for **official** PASCAL VOC evaluation only. The code now includes unofficial Python evaluation code.

### Requirements: hardware

1. For training smaller networks (ZF, VGG_CNN_M_1024) a good GPU (e.g., Titan, K20, K40, ...) with at least 3G of memory suffices
2. For training Fast R-CNN with VGG16, you'll need a K40 (~11G of memory)
3. For training the end-to-end version of Faster R-CNN with VGG16, 3G of GPU memory is sufficient (using CUDNN)

### Installation (sufficient for the demo)

1. Clone the Faster R-CNN repository
  ```Shell
  # clone
  git clone https://github.com/DFKI-Interactive-Machine-Learning/py-faster-rcnn --branch no_submodule
  ```

2. We'll call the directory that you cloned Faster R-CNN into `FRCN_ROOT`

3. Build the Cython modules
    ```Shell
    cd $FRCN_ROOT/lib
    make
    ```

4. Build Caffe and pycaffe
    ```Shell
    cd $FRCN_ROOT/caffe-fast-rcnn
    # Now follow the Caffe installation instructions here:
    #   http://caffe.berkeleyvision.org/installation.html

    # If you're experienced with Caffe and have all of the requirements installed
    # and your Makefile.config in place, then simply do:
    make -j8 && make pycaffe
    ```

5. Download pre-computed Faster R-CNN detectors
    ```Shell
    cd $FRCN_ROOT
    ./data/scripts/fetch_faster_rcnn_models.sh
    ```

    This will populate the `$FRCN_ROOT/data` folder with `faster_rcnn_models`. See `data/README.md` for details.
    These models were trained on VOC 2007 trainval.

### Demo

*After successfully completing [basic installation](#installation-sufficient-for-the-demo)*, you'll be ready to run the demo.

To run the demo
```Shell
cd $FRCN_ROOT
./tools/demo.py
```
The demo performs detection using a VGG16 network trained for detection on PASCAL VOC 2007.

### Beyond the demo: installation for training and testing models for VOC
1. Download the training, validation, test data and VOCdevkit

```Shell
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCdevkit_08-Jun-2007.tar
```

2. Extract all of these tars into one directory named `VOCdevkit`

```Shell
tar xvf VOCtrainval_06-Nov-2007.tar
tar xvf VOCtest_06-Nov-2007.tar
tar xvf VOCdevkit_08-Jun-2007.tar
```

3. It should have this basic structure

```Shell
$VOCdevkit/                           # development kit
$VOCdevkit/VOCcode/                   # VOC utility code
$VOCdevkit/VOC2007                    # image sets, annotations, etc.
# ... and several other directories ...
```

4. Create symlinks for the PASCAL VOC dataset

```Shell
cd $FRCN_ROOT/data
ln -s $VOCdevkit VOCdevkit2007
```
    Using symlinks is a good idea because you will likely want to share the same PASCAL dataset installation between multiple projects.

5. Create symlinks for the COCO dataset

```Shell
cd $FRCN_ROOT/data
ln -s <path_to_downloaded_MScoco_dataset> coco
```
    Using symlinks is a good idea because you will likely want to share the same PASCAL dataset installation between multiple projects.

5. [Optional] follow similar steps to get PASCAL VOC 2010 and 2012
6. [Optional] If you want to use COCO, please see some notes under `data/README.md`
7. Follow the next sections to download pre-trained ImageNet models

### Beyond the demo: installation for training and testing models for MSCOCO

1. Download the training, validation, test data and annotation file

```Shell
wget http://msvocds.blob.core.windows.net/coco2014/train2014.zip
wget http://msvocds.blob.core.windows.net/coco2014/val2014.zip
wget http://msvocds.blob.core.windows.net/coco2014/test2014.zip
wget http://msvocds.blob.core.windows.net/annotations-1-0-3/instances_train-val2014.zip
```

2. Extract all of these zips into one directory named `coco`

```Shell
unzip train2014.zip
unzip val2014.zip
unzip test2014.zip
unzip instances_train-val2014.zip
```
3. It should have this basic structure

```Shell
coco/                           # coco folder
coco/images/<unziped_image_train>                   # mscoco images, train
coco/images/<unziped_image_val>                    # mscoco images, val.
coco/images/<unziped_image_test>                   # mscoco images, test
coco/annotations/<unziped_train_val>               # annotation file
```
4. Create symlink for the MSCOCO dataset
```Shell
cd $FRCN_ROOT/data
ln -s <path_to_downloaded_MSCOCO_dataset> coco
```

### Available Classes To Train On (MSCOCO)
after downloading datasets and creating a symlink as described in [Beyond the demo (MSCOCO)](#beyond-the-demo-installation-for-training-and-testing-models-for-mscoco) you can run a script to find out about possible classes you can train on.
The script is located at data/MSCOCO_API_categories.py

For example : to get all classes with its ids (Note : you need the id of classes for later) call the following function : print_categories_from_name([]) and you will get the following output :

```Shell
./data/MSCOCO_API_categories.py

{u'supercategory': u'person', u'id': 1, u'name': u'person'}
{u'supercategory': u'vehicle', u'id': 2, u'name': u'bicycle'}
{u'supercategory': u'vehicle', u'id': 3, u'name': u'car'}
{u'supercategory': u'vehicle', u'id': 4, u'name': u'motorcycle'}
{u'supercategory': u'vehicle', u'id': 5, u'name': u'airplane'}
{u'supercategory': u'vehicle', u'id': 6, u'name': u'bus'}
{u'supercategory': u'vehicle', u'id': 7, u'name': u'train'}
{u'supercategory': u'vehicle', u'id': 8, u'name': u'truck'}
{u'supercategory': u'vehicle', u'id': 9, u'name': u'boat'}
{u'supercategory': u'outdoor', u'id': 10, u'name': u'traffic light'}
{u'supercategory': u'outdoor', u'id': 11, u'name': u'fire hydrant'}
{u'supercategory': u'outdoor', u'id': 13, u'name': u'stop sign'}
...
```

### Train on custom classes

After finding out your classes you want to train on [(Available Classes To Train On (MSCOCO)](#available-classes-to-train-on-mscoco), you need to do the following changes to train the classes:

open the file : experiments/cfgs/faster_rcnn_end2end.yml and fill up CAT_IDS with the ids you're interested in.

Note : if you leave the list empty it will train on all classes. Then save the file and run the end2end script

```Shell
cd $FRCN_ROOT
./expriments/scripts/faster_rcnn_end2end.sh 0 VGG_CNN_M_1024 coco
```

after creating model with specific classes you are interested in, you need only to change the model name in tools/demo.py, see the variable NETS. Then run the demo script :

```Shell
./tools/demo.py
```


### Download pre-trained ImageNet models

Pre-trained ImageNet models can be downloaded for the three networks described in the paper: ZF and VGG16.

```Shell
cd $FRCN_ROOT
./data/scripts/fetch_imagenet_models.sh
```
VGG16 comes from the [Caffe Model Zoo](https://github.com/BVLC/caffe/wiki/Model-Zoo), but is provided here for your convenience.
ZF was trained at MSRA.

### Usage

To train and test a Faster R-CNN detector using the **alternating optimization** algorithm from our NIPS 2015 paper, use `experiments/scripts/faster_rcnn_alt_opt.sh`.
Output is written underneath `$FRCN_ROOT/output`.

```Shell
cd $FRCN_ROOT
./experiments/scripts/faster_rcnn_alt_opt.sh [GPU_ID] [NET] [--set ...]
# GPU_ID is the GPU you want to train on
# NET in {ZF, VGG_CNN_M_1024, VGG16} is the network arch to use
# --set ... allows you to specify fast_rcnn.config options, e.g.
#   --set EXP_DIR seed_rng1701 RNG_SEED 1701
```

("alt opt" refers to the alternating optimization training algorithm described in the NIPS paper.)

To train and test a Faster R-CNN detector using the **approximate joint training** method, use `experiments/scripts/faster_rcnn_end2end.sh`.
Output is written underneath `$FRCN_ROOT/output`.

```Shell
cd $FRCN_ROOT
./experiments/scripts/faster_rcnn_end2end.sh [GPU_ID] [NET] [--set ...]
# GPU_ID is the GPU you want to train on
# NET in {ZF, VGG_CNN_M_1024, VGG16} is the network arch to use
# --set ... allows you to specify fast_rcnn.config options, e.g.
#   --set EXP_DIR seed_rng1701 RNG_SEED 1701
```

This method trains the RPN module jointly with the Fast R-CNN network, rather than alternating between training the two. It results in faster (~ 1.5x speedup) training times and similar detection accuracy. See these [slides](https://www.dropbox.com/s/xtr4yd4i5e0vw8g/iccv15_tutorial_training_rbg.pdf?dl=0) for more details.

Artifacts generated by the scripts in `tools` are written in this directory.

Trained Fast R-CNN networks are saved under:

```
output/<experiment directory>/<dataset name>/
```

Test outputs are saved under:

```
output/<experiment directory>/<dataset name>/<network snapshot name>/
```

