from detectron2.config import CfgNode as CN


def add_dd3d_config(cfg):
    """
    Add config for DD3D.
    """
    # print("cfg", cfg)
    cfg.DATASETS.TRAIN = CN()
    cfg.DATASETS.TEST = CN()
    cfg.INPUT.RANDOM_FLIP = CN()
    cfg.set_new_allowed(True)

    cfg.MODEL.META_ARCHITECTURE = "DD3D"
    cfg.MODEL.CKPT = ""

    cfg.FE = CN()
    cfg.FE.FPN = CN()
    cfg.FE.FPN.IN_FEATURES = ["level3", "level4", "level5"]
    cfg.FE.FPN.OUT_FEATURES = None
    cfg.FE.FPN.OUT_CHANNELS = 256
    cfg.FE.FPN.NORM = "FrozenBN"
    cfg.FE.FPN.FUSE_TYPE = "sum"
    cfg.FE.BUILDER = "build_fcos_dla_fpn_backbone_p67"
    cfg.FE.BACKBONE = CN()
    cfg.FE.BACKBONE.NAME = "DLA-34"
    cfg.FE.BACKBONE.OUT_FEATURES = ["level3", "level4", "level5"]
    cfg.FE.BACKBONE.NORM = "FrozenBN"
    cfg.FE.OUT_FEATURES = None
    cfg.DD3D = CN()
    cfg.DD3D.IN_FEATURES = None
    cfg.DD3D.NUM_CLASSES = 5
    cfg.DD3D.FEATURE_LOCATIONS_OFFSET = None
    cfg.DD3D.SIZES_OF_INTEREST = [64, 128, 256, 512]
    cfg.DD3D.INFERENCE = CN()
    cfg.DD3D.INFERENCE.DO_NMS = True
    cfg.DD3D.INFERENCE.DO_POSTPROCESS = True
    cfg.DD3D.INFERENCE.DO_BEV_NMS = False
    cfg.DD3D.INFERENCE.BEV_NMS_IOU_THRESH = 0.3
    cfg.DD3D.INFERENCE.NUSC_SAMPLE_AGGREGATE = False
    cfg.DD3D.FCOS2D = CN()
    cfg.DD3D.FCOS2D._VERSION = "v2"
    cfg.DD3D.FCOS2D.NORM = "BN"
    cfg.DD3D.FCOS2D.NUM_CLS_CONVS = 4
    cfg.DD3D.FCOS2D.NUM_BOX_CONVS = 4
    cfg.DD3D.FCOS2D.USE_SCALE = True
    cfg.DD3D.FCOS2D.USE_DEFORMABLE = False
    cfg.DD3D.FCOS2D.BOX2D_SCALE_INIT_FACTOR = 1.0
    cfg.DD3D.FCOS2D.LOSS = CN()
    cfg.DD3D.FCOS2D.LOSS.ALPHA = 0.25
    cfg.DD3D.FCOS2D.LOSS.GAMMA = 2.0
    cfg.DD3D.FCOS2D.LOSS.LOC_LOSS_TYPE = "giou"
    cfg.DD3D.FCOS2D.INFERENCE = CN()
    cfg.DD3D.FCOS2D.INFERENCE.THRESH_WITH_CTR = True
    cfg.DD3D.FCOS2D.INFERENCE.PRE_NMS_THRESH = 0.05
    cfg.DD3D.FCOS2D.INFERENCE.PRE_NMS_TOPK = 1000
    cfg.DD3D.FCOS2D.INFERENCE.POST_NMS_TOPK = 100
    cfg.DD3D.FCOS2D.INFERENCE.NMS_THRESH = 0.75
    cfg.DD3D.FCOS3D = CN()
    cfg.DD3D.FCOS3D.NORM = "FrozenBN"
    cfg.DD3D.FCOS3D.NUM_CONVS = 4
    cfg.DD3D.FCOS3D.USE_DEFORMABLE = False
    cfg.DD3D.FCOS3D.USE_SCALE = True
    cfg.DD3D.FCOS3D.DEPTH_SCALE_INIT_FACTOR = 0.3
    cfg.DD3D.FCOS3D.PROJ_CTR_SCALE_INIT_FACTOR = 1.0
    cfg.DD3D.FCOS3D.PER_LEVEL_PREDICTORS = False
    cfg.DD3D.FCOS3D.SCALE_DEPTH_BY_FOCAL_LENGTHS = True
    cfg.DD3D.FCOS3D.SCALE_DEPTH_BY_FOCAL_LENGTHS_FACTOR = 500.0
    cfg.DD3D.FCOS3D.MEAN_DEPTH_PER_LEVEL = [32.594, 15.178, 8.424, 5.004, 4.662]
    cfg.DD3D.FCOS3D.STD_DEPTH_PER_LEVEL = [14.682, 7.139, 4.345, 2.399, 2.587]
    cfg.DD3D.FCOS3D.MIN_DEPTH = 0.1
    cfg.DD3D.FCOS3D.MAX_DEPTH = 80.0
    cfg.DD3D.FCOS3D.CANONICAL_BOX3D_SIZES = [
        [1.61876949, 3.89154523, 1.52969237],
        [0.62806586, 0.82038497, 1.76784787],
        [0.56898187, 1.77149234, 1.7237099],
        [1.9134491, 5.15499603, 2.18998422],
        [2.61168401, 9.22692319, 3.36492722],
        [0.5390196, 1.08098042, 1.28392158],
        [2.36044838, 15.56991038, 3.5289238],
        [1.24489164, 2.51495357, 1.61402478],
    ]
    cfg.DD3D.FCOS3D.CLASS_AGNOSTIC_BOX3D = False
    cfg.DD3D.FCOS3D.PREDICT_ALLOCENTRIC_ROT = True
    cfg.DD3D.FCOS3D.PREDICT_DISTANCE = False
    cfg.DD3D.FCOS3D.LOSS = CN()
    cfg.DD3D.FCOS3D.LOSS.SMOOTH_L1_BETA = 0.05
    cfg.DD3D.FCOS3D.LOSS.MAX_LOSS_PER_GROUP_DISENT = 20.0
    cfg.DD3D.FCOS3D.LOSS.CONF_3D_TEMPERATURE = 1.0
    cfg.DD3D.FCOS3D.LOSS.WEIGHT_BOX3D = 2.0
    cfg.DD3D.FCOS3D.LOSS.WEIGHT_CONF3D = 1.0
    cfg.DD3D.FCOS3D.PREPARE_TARGET = CN()
    cfg.DD3D.FCOS3D.PREPARE_TARGET.CENTER_SAMPLE = True
    cfg.DD3D.FCOS3D.PREPARE_TARGET.POS_RADIUS = 1.5
    cfg.MODEL = CN()
    cfg.MODEL.DEVICE = "cuda"
    cfg.MODEL.META_ARCHITECTURE = "DD3D"
    cfg.MODEL.PIXEL_MEAN = [103.53, 116.28, 123.675]
    cfg.MODEL.PIXEL_STD = [57.375, 57.12, 58.395]
    cfg.MODEL.CKPT = ""
    cfg.MODEL.BOX2D_ON = True
    cfg.MODEL.BOX3D_ON = True
    cfg.MODEL.DEPTH_ON = False
    cfg.MODEL.WEIGHTS = ""
