import io
import base64
from PIL import Image
from filters import *

def get_img_download(img,filename,text):
    buffered = io.BytesIO()
    img.save(buffered,format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href= f'<a href="data:file/txt;base64,{img_str}" download = "{filename}">{text}</a>'
    return href
#Set title
st.title('Image Filters')    

#Upload Images
uploaded_file = st.file_uploader("Choose an image file:",type=['jpg','jpeg','png'])

if uploaded_file is not None:
    raw_bytes = np.asarray(bytearray(uploaded_file.read()),dtype=np.uint8)
    img = cv2.imdecode(raw_bytes,cv2.IMREAD_COLOR)
    input_col,output_col = st.columns(2)
    
    with input_col:
        st.header("Original")
        st.image(img,channels="BGR",use_column_width=True)
    st.header("Filter Examples")
    option = st.selectbox("Select a filter: ",('None','Black and White','Vintage','Vignette Effect','Pencil Sketch','Embossed','sketch_filter','cartoon_filter'))

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.caption("Black and White")
        st.image("bw.jpg")
    with col2:
        st.caption("Cartoon Filter")
        st.image("cartoon.jpg")
    with col3:
        st.caption("Sepia Effect")
        st.image("sepia.jpg")
    with col4:
        st.caption("Pencil Sketch")
        st.image('pencil.jpg')
    output_flag=1
    color = "BGR"

    #Generate filtered image based on the selected option                    
    if option=='None':
        output_flag=0
    elif option=='Black and White':
        output=bw_filter(img)
        color = 'GRAY'
    elif option=='Vintage':
        output = sepia(img)
    elif option=='Vignette Effect':
        level = st.slider("Level",0,5,2)
        output = vignette(img,level)
    elif option == 'Pencil Sketch':
        #ksize= st.slider("Blur Kernel Size",1,11,5,step=2)
        output = pencil_sketch(img)
        color= 'GRAY'
    elif option=='Embossed':
        output = embossed_edges(img) 
    elif option=='sketch_filter':
        output = sketch_filter(img)
        color = 'GRAY'
    elif option=='cartoon_filter':
        output = cartoon_filter(img)               

    with output_col:
        if output_flag==1:
            st.header("Output")
            st.image(output,channels=color)
            if color =='BGR':
                result = Image.fromarray(output[:,:,::-1])
            else:
                result = Image.fromarray(output)

            #Display the link
            st.markdown(get_img_download(result,'output.png','Download'+'Output'),unsafe_allow_html=True)         

