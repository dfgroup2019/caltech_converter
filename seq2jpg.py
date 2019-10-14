import cv2
import os


def seq_video_read(path):

    pathdir = os.listdir(path)
    for i in pathdir:
        print(i)
        newdir = os.path.join(path,i)
        if os.path.splitext(newdir)[1]==".seq":
            print(newdir)
            cap = cv2.VideoCapture(newdir)
            while(1):
                ret,frame = cap.read()
                if ret == True:
                    cv2.imshow("test",frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()



def seq2jpg(input_dir,output_dir):

    video_dir = os.listdir(input_dir)
    for i in video_dir:
        c=0
        newdir = os.path.join(input_dir,i)
        if os.path.splitext(newdir)[1]==".seq":
            
            
            folder_name = os.path.splitext(i)[0]
            #print("folder_name = ",folder_name)
            new_output_dir = os.path.join(output_dir,folder_name)
            print(new_output_dir)
            folder = os.path.exists(new_output_dir)
            if not folder:
                os.mkdir(new_output_dir)
            else:
                print("---There is this folder!---")
            if os.path.splitext(newdir)[1]==".seq":
                
                vc = cv2.VideoCapture(newdir)
                rval = vc.isOpened()
                while rval:
                    c = c + 1
                    ret,frame = vc.read()
                    if ret == True:
                        cv2.imwrite(new_output_dir +'\\' + str(c) +'.jpg',frame)
                        cv2.waitKey(1)
                    else:
                        break
                vc.release()
                


if __name__ == '__main__':

    read_path = r'E:\\traffic participant\\caltech_data\\set00'
    #seq_video_read(read_path)    #读取并显示seq视频流

    save_path = 'E:\\traffic participant\\caltech_data\\seq2jpg'
    seq2jpg(read_path,save_path)  #读取并将seq视频转换为jpg图片
    

            
