import os
from collections import Counter
import subprocess
import uuid

class_map_dict = {'0':'neutral','1':'happy','2':'open palms','3':'hand collab','4':'No eye contact','5':'Confident'}

def get_results_summary(labels_file_path):
    text_file_list = list(map(lambda x:os.path.join(labels_file_path,x),os.listdir(labels_file_path)))
    class_count = []
    for file in text_file_list:
        with open(file,'r') as fp:
            data = fp.readlines()
        data = [i.split(' ')[0] for i in data]
        class_count.extend(data) #[0,0,5,2,3,1,5] => {'0':0.70,'5':2}
    d = {}
    for i,j in dict(Counter(class_count)).items():
        d[class_map_dict[i]] = (j/len(text_file_list))
    return d

def run_detection(weights, source, conf, save_txt, save_conf, save_crop, project, name):
    os.makedirs(os.path.join(project, name), exist_ok=True)
    
    command = [
        'python', 'detect.py',
        '--weights', weights,
        '--source', source,
        '--conf', str(conf),
    ]

    if save_txt:
        command.append('--save-txt')
    if save_conf:
        command.append('--save-conf')
    if save_crop:
        command.append('--save-crop')

    command.extend(['--project', project, '--name', name])
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
    if result.returncode != 0:
        print(f"Error running detection: {result.stderr}")
        return None

    name = name + '2'
    # Construct the path to the label file
    label_file_path = os.path.join(project, name, 'labels')
    video_file_path = os.path.join(os.path.join(project, name), os.path.basename(source))
    
    print('label_file_path: ',label_file_path)
    print('video_file_path: ',video_file_path)
    
    convertedVideo = os.path.join(os.path.join(project, name),'output2.mp4')
    subprocess.call(args=f"ffmpeg -y -i {video_file_path} -c:v libx264 {convertedVideo}".split(" "))
    return label_file_path,convertedVideo

if __name__ == '__main__':
    label_file,video_file_path = run_detection(
        weights='best.pt',
        source='test_vid_1_trim.mp4',
        conf=0.25,
        save_txt=True,
        save_conf=True,
        save_crop=False,
        project='results_dir',
        name=uuid.uuid4().hex #datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    )
    # label_file = label_file + '2'
    if label_file:
        print(f"Label file path: {label_file}")
    else:
        print("Label file not found.")
    
    # labels_file_path = 'yolov5/runs/detect/exp7/labels'
    d = get_results_summary(label_file)
    print(d)