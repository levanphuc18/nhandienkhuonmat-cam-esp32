import shutil
import csv
import inspect
import tkinter as tk
import cv2, os
import numpy as np
import pandas as pd
import datetime
import time
import urllib.request
import face_recognition

# Thay đổi đường dẫn
path = r'/Users/levan/PycharmProjects/pythonProject6/f_IOT_nhandienkhuonmat/TrainingImage'
url='http://192.168.89.51/cam-hi.jpg'


#lấy thư mục hiện tại
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Dòng này tạo một đối tượng Tkinter, là cửa sổ gốc của ứng dụng GUI.
window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser")
dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

# answer = messagebox.askquestion(dialog_title, dialog_text)

window.geometry('1450x750')
# màu xanh trung bình
window.configure(background='medium sea green')


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)



def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text= res)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



          # TẠO FORM
message = tk.Label(window, text="ĐIỂM DANH VỚI NHẬN DIỆN KHUÔN MẶT" ,bg="Green"  ,fg="white"  ,width=50  ,height=3,font=('times', 30))

message.place(x=200, y=20)

lbl = tk.Label(window, text="Nhập ID",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') )
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20  ,bg="white" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Nhập Tên",width=20  ,fg="red"  ,bg="yellow"    ,height=2 ,font=('times', 15, ' bold '))
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20  ,bg="white"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)

lbl3 = tk.Label(window, text="Thông Báo : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold underline '))
lbl3.place(x=400, y=400)

message = tk.Label(window, text="" ,bg="white"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
message.place(x=700, y=400)

lbl3 = tk.Label(window, text="Trường Hợp Có Mặt : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold  underline'))
lbl3.place(x=100, y=650)

lbl3 = tk.Label(window, text="Sỉ Số : ",width=10  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold  underline'))
lbl3.place(x=850, y=650)

message2 = tk.Label(window, text="" ,fg="red"   ,bg="white",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold '))
message2.place(x=370, y=650)

message3 = tk.Label(window, text="" ,fg="red"   ,bg="white",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold '))
message3.place(x=1000, y=650)

            # TẠO FORM


#chụp ảnh để train
def TakeImages():
    Id=(txt.get())
    name=(txt2.get())
    print(Id)

    def get_all_ids_from_folder(folder_path):
        # Lấy danh sách các thư mục trong đường dẫn
        subdirectories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

        # Khởi tạo danh sách để lưu trữ các ID
        ids = set()

        for subdirectory in subdirectories:
            # Lấy ID từ tên thư mục (ở đây tôi giả sử rằng ID là phần đầu của tên thư mục)
            Id = int(subdirectory.split("_")[0])
            ids.add(Id)

        return list(ids)

    # Sử dụng hàm để lấy danh sách các ID từ thư mục
    all_ids = get_all_ids_from_folder("TrainingImage")

    # In danh sách các ID
    id_string = ', '.join(map(str, all_ids))
    print("Danh sách các String ID: [" + id_string + "]")



    # Kiểm tra ID ảnh có trùng hay không
    if Id in id_string:
        strId = str(Id)
        res = "ID " + strId + " đã được sử dụng"
        message.configure(text=res)
        print(f"ID {strId} đã xuất hiện trước đó.")
    else:
        print("Id chưa bị trùng lặp")
    # Kiểm tra ID ảnh có trùng hay không

    # Kiểm tra ID ảnh có trùng hay không
    def is_id_unique(az, ad):
        if az in ad:
            strId = str(az)
            res = "ID " + strId + " đã được sử dụng"
            return False
        else:
            return True



    # Ktra xem ô ID và Name có đúng định dạng k
    if (is_number(Id) and name.isalpha() and is_id_unique(Id,id_string)):
        cam = cv2.VideoCapture(0) # Camera ma tính

        # Đây là đường dẫn tới tệp XML chứa thông tin về mô hình phát hiện khuôn mặt.
        harcascadePath = "haarcascade_frontalface_default.xml"
        # Tạo 1 đối tượng CascadeClassifier dùng để phát hiện khun mặt
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0


        # bắt đầu chụp ảnh
        while (True):
            # Camera máy tính
            # ret, img = cam.read()

            # Camera esp32
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgnp, -1)

            # Tìm khuôn mặt trong cam
            faces = detector.detectMultiScale(img, 1.3, 5)
            cv2.imshow('frame', img)
            # Chụp ảnh và lưu vào thư mục TrainingImage
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Đổi kích thước ảnh về 300x330
                resized_face = cv2.resize(img[y:y + h, x:x + w], (300, 330))
                # incrementing sample number
                sampleNum = sampleNum + 1
                # TrainingImageTemp dùng để train và đưa tất cả ảnh vừa train vào cùng 1 thư mục
                cv2.imwrite("TrainingImageTemp\\" + Id + "_" + name + '_' + str(sampleNum) + ".jpg",
                            resized_face)
                # display the frame
                cv2.imshow('frame', img)

            # dừng khi ấn "q" hoặc số ảnh chụp >100
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 5:
                break
#        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]

        # mở file csv và thêm 1 sv vào
        with open('StudentDetails\\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if (is_number(Id)):
            res = "Nhập tên theo bảng chữ cái"
            message.configure(text=res)
        if (name.isalpha()):
            res = "Nhập ID là sô"
            message.configure(text=res)

        # Kiểm tra ID ảnh có trùng hay không
        if (name.isalpha() and is_number(Id)):
            res = "Id đã được sử dụng"
            message.configure(text=res)
        # Kiểm tra ID ảnh có trùng hay không



# Hàm di chuyển các file train sang folder
def MoveFile(source, destination):
    shutil.move(source, destination)


#train các ảnh đã chụp
def TrainImages():
    # Chạy vòng for đưa hết ảnh ở train tạm sang DoneTrain
    for imageDone in os.listdir('TrainingImageTemp\\'):
        destination_folder = os.path.join(CurDir, "TrainingImage", str(txt.get()) + "_" + str(txt2.get()))
        # Tạo thư mục đích nếu nó không tồn tại
        os.makedirs(destination_folder, exist_ok=True)
        destination_path = os.path.join(destination_folder, imageDone)
        MoveFile(os.path.join(CurDir, "TrainingImageTemp", imageDone), destination_path)
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

# Đếm tổng số lượng sinh viên
def count_sv(directory):
    if not os.path.exists(directory):
        return 0
    SiSoSinhVien = 0
    for root, dirs, files in os.walk(directory):
        SiSoSinhVien += len(dirs)
    return SiSoSinhVien
# Đếm tổng số lượng sinh viên




cam = cv2.VideoCapture(0)
#nhận diện khuôn mặt trên CAMERA
def TrackImages():
    # IOT
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)

    def findEncodings(images, classNames):
        print("Xóa các ảnh không tìm thấy khuôn mặt trước khi khởi động lại chương trình: \n")
        encodeList = []
        for img, className in zip(images, classNames):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Tìm kiếm tất cả các khuôn mặt trong ảnh
            face_locations = face_recognition.face_locations(img)

            if len(face_locations) > 0:
                # Nếu có ít nhất một khuôn mặt, thực hiện trích xuất vector đặc trưng của khuôn mặt đầu tiên
                encode = face_recognition.face_encodings(img, face_locations)[0]
                encodeList.append(encode)
            else:
                print(f"Không tìm thấy khuôn mặt trong ảnh {className}.")
                res = "Lỗi!!Xóa ảnh k tìm thấy khuôn mặt"
                message.configure(text=res)
                continue
        return encodeList

    for root, dirs, files in os.walk(path):
        for cl in files:
            curImg = cv2.imread(os.path.join(root, cl))
            # resize tất cả ảnh về cùng 1 kích thước để lưu vào mảng numpy
            curImg = cv2.resize(curImg, (300, 300))
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

    # Chuyển danh sách thành mảng NumPy
    images_array = np.array(images)
    classNames_array = np.array(classNames)

    np.save('olivetti_faces.npy', images_array)

    # Đọc dữ liệu từ tệp .npy
    faces_data = np.load('olivetti_faces.npy')

    # Sử dụng dữ liệu đọc được để huấn luyện mô hình
    encodeListKnown = findEncodings(faces_data, classNames)

        #IOT

    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    # Thực hiện vòng lặp vô hạn để liên tục nhận diện khuôn mặt từ máy ảnh.
    while True:
        # Camera máy tính
        # ret, img = cam.read()

        # Camera esp32
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            print("Face Detected")
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()

                # Tách tên file và lấy phần cần thiết
                parts = name.split("_")
                if len(parts) >= 2:
                    name_new = "_".join(parts[:2])
                else:
                    name_new = name

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                Id = parts[0]
                Name = parts[1]

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name_new, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                attendance.loc[len(attendance)] = [Id, Name, date, timeStamp]

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', img)
        if (cv2.waitKey(1) == ord('q')):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName = "Attendance\\Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    attendance.to_csv(fileName,index=False)
#    cam.release()
    cv2.destroyAllWindows()

    # Đếm số lượng dòng trong file csv -> số sinh viên có mặt
    SV_Attendance = attendance.shape[0]
    print(f"Số sinh viên có mặt: {SV_Attendance}")

    # Chuyển sang kiểu chuỗi đưa vào Message3
    SoSvThamGia = str(SV_Attendance)

    # Đếm số lượng sv
    SiSoSinhVien = count_sv("TrainingImage\\")
    print(f"Tổng số lượng sinh viên: {SiSoSinhVien}")

    # Chuyển sang kiểu chuổi đưa vào Message3
    TongsisoSV = str(SiSoSinhVien)

    res1 = "Sỉ số: " + SoSvThamGia + "/" + TongsisoSV
    message3.configure(text=res1)
    # Đếm số lượng sv

    print(attendance)
    #print(attendance)
    res=attendance
    message2.configure(text= res)


# đóng cửa sổ xóa hết ảnh trong thư mục train tránh bị trùng ảnh
def close_window():
    # Xóa tất cả các tệp ảnh trong thư mục trainingImageTemp
    directory_path = "TrainingImageTemp\\"
    file_list = os.listdir(directory_path)
    for file in file_list:
        file_path = os.path.join(directory_path, file)
        os.remove(file_path)
    print("\n Đã xóa hết ảnh trong TrainingImageTemp")
    # Đóng cửa sổ
    window.destroy()


clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)
takeImg = tk.Button(window, text="Lấy Ảnh Mẫu", command=TakeImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Ảnh", command=TrainImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Nhận Diện", command=TrackImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=800, y=500)
quitWindow = tk.Button(window, text="Thoát", command=close_window  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=500)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Ashish","", "TEAM", "superscript")
copyWrite.configure(state="disabled",fg="red"  )
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)

window.mainloop()