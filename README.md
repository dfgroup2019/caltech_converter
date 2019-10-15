# caltech数据集
从车辆前视摄像头记录的一组数据，相比之前下载的Stanford Drone Dataset，每帧图像有十几个行人却只打了两三个行人的标签，caltech数据集行人的标签打得更加仔细，在学习中更好用。并且是运动中的车辆的前视摄像头记录的，视角对我们来说更有用。但是在处理Caltech数据集时发现他的视频数据是seq形式的，标签数据是vbb格式的，拿来学习的话不是很好用，所以进行了一下格式转换

# seq2jpg

1、修改seq2jpg.py文件中的read_path和save_path，read_path为*.seq文件所在文件夹，save_path为jpg图片保存文件夹

2、运行seq2jpg.py

# vbb2xml

1、修改vbb2xml.py文件中的vbb_inputdir和vbb_outputdir，vbb_inputdir为set00，set01……所在文件夹，vbb_outputdir为xml文件输出文件夹

2、运行vbb2xml.py
