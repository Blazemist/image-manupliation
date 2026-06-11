from PIL import Image,ImageTk
import io
from tkinter import ttk,filedialog,messagebox,Tk

image_path, window = None,None
Images ,Labels ,Buttons ,Entries , Messageboxs = {},{},{},{},{}
def select_photo():
    global image_path
    file = filedialog.askopenfile(
        title='Select your picture',
        filetypes=[
            ('PNG Files', '*.png'),
            ('JPG/JPEG Files', '*.jpg *.jpeg'),
            ("IMAGE Files", '*.png *.jpg *.jpeg'),
            ("ALL FIles", "*.*")
            ])
    if not file:
        return
    image_path = file.name
    Images['img'] = Image.open(image_path)
    Images['display']= Images['img'].resize((490,290))
    Images['display'] = ImageTk.PhotoImage(Images['display'])
    Labels['display_image'] = ttk.Label(window,image=Images['display'],relief='solid')
    Buttons['Proceed'] = ttk.Button(window,text='Proceed',command=type_selection)
    Labels['display_image'].place(x=1,y=75)
    Buttons['Proceed'].place(x=320,y=400)
    Buttons['select'].place(x=120,y=400)


def type_selection():
    Buttons['select'].destroy()
    Buttons['Proceed'].destroy()
    Buttons['dim'] = ttk.Button(window,text='Reduce dimension',command=red_dim)
    Buttons['kb'] = ttk.Button(window,text='Reduce kb',command=red_kb)
    Buttons['dim'].place(x=100,y=400)
    Buttons['kb'].place(x=300,y=400)

def red_dim(): 
    Buttons['dim'].destroy()
    Buttons['kb'].destroy()
    Labels['height'] = ttk.Label(window,text= 'Enter Height:  ',relief='raised')
    Labels['width'] = ttk.Label(window,text= 'Enter width: ',relief='raised')
    Buttons['dim_confirm'] = ttk.Button(window,text='Confirm',command=photo_resize)
    Entries['height'] = ttk.Entry(window)
    Entries['width'] = ttk.Entry(window)
    Entries['height'].place(x=175,y=390)
    Entries['width'].place(x=175,y=410)
    Labels['height'].place(x=100,y=390)
    Labels['width'].place(x=100,y=410)
    Buttons['dim_confirm'].place(x=200,y=430)
    

def photo_resize():
    w,h = Images['img'].size
    new_w = int(Entries['width'].get())
    new_h = int(Entries['height'].get())
    if w < new_w or h < new_h:
        Messageboxs['invalid_dim'] = messagebox.showerror(
            title='Invalid Dimenstion',message='height and width\nmust be less\nthan images')
    else:
        Entries['height'].destroy()
        Entries['width'].destroy()
        Labels['height'].destroy()
        Labels['width'].destroy()
        Buttons['dim_confirm'].destroy()
        path = image_path[:image_path.rfind('.')]+'_resized'+image_path[image_path.rfind('.'):]
        Labels['confirmation'] = ttk.Label(window,text=f'image saved at {path}')
        Images['resize_img'] = Images['img'].resize((new_w,new_h))
        Images['resize_img'].save(path)
        Labels['confirmation'].place(x=0,y=400)

def red_kb():
    Buttons['dim'].destroy()
    Buttons['kb'].destroy()
    Labels['kb'] = ttk.Label(window,text= 'Enter Kb:  ',relief='raised')
    Entries['kb'] = ttk.Entry(window)
    Buttons['kb_confirm'] = ttk.Button(window,text='Confirm',command=photo_reduc)
    Entries['kb'].place(x=175,y=390)
    Labels['kb'].place(x=100,y=390)
    Buttons['kb_confirm'].place(x=200,y=410)

def photo_reduc():
    buffer = io.BytesIO()
    Images['img'].save(buffer,format=image_path[image_path.rfind('.'):])
    current = buffer.tell()/1024
    target = int(Entries['kb'].get())*0.8
    w,h = Images['img'].size
    counter = 1
    if current<target:
        Messageboxs['invalid_size'] = messagebox.showerror(
            title='Invalid Size',
            message='Size can only be reduced'
            )
    else:
        Entries['kb'].destroy()
        Labels['kb'].destroy()
        Buttons['kb_confirm'].destroy()
        while current >= target and counter <= 100:
            buffer.truncate(0)
            buffer.seek(0)
            ratio = (target/current)**0.5
            w = int(w*ratio)
            h = int(h*ratio)
            Images['img']= Images['img'].resize((w,h))
            Images['img'].save(buffer,format='PNG')
            current = buffer.tell()/1024
            counter+=1
        path = image_path[:image_path.rfind('.')]+'_compressed'+image_path[image_path.rfind('.'):]
        Labels['confirmation'] = ttk.Label(window,text=f'image saved at {path}')
        Images['img'].save(path)
        Labels['confirmation'].place(x=0,y=400)

        
window = Tk(className='Photo compressor')
window.geometry('500x500')
window.resizable(False,False)
Labels['title'] = ttk.Label(window,text='Photo compressor & resizer',relief='raised')
Buttons['select'] = ttk.Button(window,text='Choose image',command=select_photo)
Buttons['quit'] = ttk.Button(window,text='quit',command=lambda : window.destroy())
Labels['title'].place(x=175,y=50)
Buttons['select'].place(x=200,y=200)
Buttons['quit'].place(x=200,y=450)
window.mainloop()
