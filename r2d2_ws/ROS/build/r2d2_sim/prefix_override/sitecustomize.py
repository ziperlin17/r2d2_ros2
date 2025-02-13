import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ziper/r2d2_ws_last/r2d2_ws/ROS/install/r2d2_sim'
