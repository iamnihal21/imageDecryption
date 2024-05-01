import streamlit as st
from PIL import Image
import os

# Convert encoding data into 8-bit binary form using ASCII value of characters
def genData(data):
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                  imdata.__next__()[:3] +
                                  imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0):
                if (pix[j]% 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode_text(image_path, data, new_image_path):
    image = Image.open(image_path, 'r')
    newimg = image.copy()
    print("Image:", newimg)
    print("Data:", data)
    encode_enc(newimg, data)
    newimg.save(new_image_path, str(new_image_path.split(".")[1].upper()))

def decode_text(image_path):
    image = Image.open(image_path, 'r')
    imgdata = iter(image.getdata())
    data = ''
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def main():
    st.title("Steganography App")

    option = st.sidebar.selectbox(
        "Select an option:",
        ("Encode", "Decode")
    )

    if option == "Encode":
        st.header("Encode Text in Image")
        image_file = st.file_uploader("Upload image:", type=["jpg", "jpeg", "png"])
        text = st.text_area("Enter text to encode:")

        if st.button("Encode"):
            if image_file is not None and text:
                new_image_path = os.path.join("uploads", "encoded_image.png")
                encode_text(image_file, text, new_image_path)
                st.success("Text encoded successfully! You can download the encoded image below.")
                st.image(new_image_path, caption="Encoded Image", use_column_width=True)
            else:
                st.error("Please upload an image and enter text to encode.")

    elif option == "Decode":
        st.header("Decode Text from Image")
        encoded_image_file = st.file_uploader("Upload encoded image:", type=["jpg", "jpeg", "png"])

        if st.button("Decode"):
            if encoded_image_file is not None:
                decoded_text = decode_text(encoded_image_file)
                st.success("Text decoded successfully!")
                st.write("Decoded Text:")
                st.write(decoded_text)
            else:
                st.error("Please upload an encoded image.")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
