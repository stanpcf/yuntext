#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
from tensorflow import flags

from data_process import get_data, cfg

# model relation
flags.DEFINE_string('classifier', 'bidirectional_lstm.BiLSTM', "path of the Class for the classifier")
flags.DEFINE_integer('nb_epoch', 50, "number of epoch")
flags.DEFINE_integer('embed_size', 300, "hidden size of embedding layer")
flags.DEFINE_string('last_act', 'softmax', "the activation for the last layer")
flags.DEFINE_integer('batch_size', 640, "batch size for train")
flags.DEFINE_string('optimizer', 'adam', "the optimizer for train")
flags.DEFINE_bool('use_pretrained', True, "if use pretrained vector for embedding layer")
flags.DEFINE_bool('trainable', True,
                  "if the embedding layer is trainable. this param is used only `use_pretrained` is true")
flags.DEFINE_integer("conv_kernel", 3, "kernel size of TextCNN")
flags.DEFINE_integer("num_class", 5, "the number of class for classify")

# data relation
flags.DEFINE_float('train_size', 0.8, "the rate of train-valid split for train data set")
flags.DEFINE_integer('max_len', 80, "regular sentence to a fixed length")
flags.DEFINE_bool('one_hot', True, "one-hot encode the label")
flags.DEFINE_bool('sum_prob', False, "是否将网络概率相加")
flags.DEFINE_bool("set_cls_weight", True, "if set class weights for sample， default true")
flags.DEFINE_string("cls_weights", "8_8_4_1.4_1", "set class weights for train data")
flags.DEFINE_string("cut_tool", 'jieba',
                    "use the cut tool's split as input. optional cut tool has fool_jieba_pynlpir_thulac. "
                    "if use some of this, use '_' to connect those. if 'all', use all cut_tools. ")
flags.DEFINE_bool("serial", False, "是否将数据训练数据串行")
flags.DEFINE_bool('enhance', False, "是否数据增强")

FLAGS = flags.FLAGS
print("one_hot:", FLAGS.one_hot)
print("sum_prob:", FLAGS.sum_prob)


def main():
    data = get_data(train_size=FLAGS.train_size, max_len=FLAGS.max_len, set_cls_weight=FLAGS.set_cls_weight,
                    cut_tool=FLAGS.cut_tool, serial=FLAGS.serial, enhance_sent=FLAGS.enhance,
                    cls_weights_str=FLAGS.cls_weights, num_class=FLAGS.num_class, one_hot=FLAGS.one_hot)

    cls_name = FLAGS.classifier
    module_name = ".".join(cls_name.split('.')[:-1])
    cls_name = cls_name.split('.')[-1]
    _module = importlib.import_module(module_name)
    cls = _module.__dict__.get(cls_name)

    model = cls(data=data, nb_epoch=FLAGS.nb_epoch, max_len=FLAGS.max_len, embed_size=FLAGS.embed_size,
                last_act=FLAGS.last_act, batch_size=FLAGS.batch_size, optimizer=FLAGS.optimizer,
                use_pretrained=FLAGS.use_pretrained, trainable=FLAGS.trainable, filter_window=FLAGS.conv_kernel,
                num_class=FLAGS.num_class, one_hot=FLAGS.one_hot,
                sum_prob=FLAGS.sum_prob)

    model.train()
    model.predict()


if __name__ == '__main__':
    main()
